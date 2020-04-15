import csv
from typing import Dict


def print_results(results, file_name, all):
    with open(file_name, "w+") as out:
        writer = csv.DictWriter(out, ["Ответ", "Процент", "Сколько"])
        writer.writeheader()
        for answer, number in results.items():
            writer.writerow({"Ответ": answer, "Процент": number / all * 100, "Сколько": number})


males = 0
male_answers = {}
fem_answers = {}
females = 0

with open("anna_research.csv", mode="r", encoding="UTF-8") as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        target_answers = \
            list(
                map(
                    lambda it: str(it),
                    str(
                        line["В чем Вы видите ценность брака? Выберите сновные достоинства брака (не более 3-х)."]
                    ).split(";")
                )
            )
        male = line["Пол"] == "Мужской"
        target_dict = male_answers if male else fem_answers
        if male :
            males += 1
        else:
            females += 1
        for answer in target_answers:
            target_dict[answer] = target_dict.get(answer, 0) + 1

print_results(male_answers, "males.csv", males)
print_results(fem_answers, "females.csv", females)

# with open("res.csv", mode="w+") as out:


