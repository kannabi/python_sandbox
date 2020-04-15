import json
import xml.etree.ElementTree as ET
import re
from typing import Set, List


class WordCleaner:
    _regex = re.compile('[^a-zA-Z\']')

    def clean(self, word):
        return self._regex.sub('', word)


def extract_unique_words(cleaner: WordCleaner, text: str) -> List[str]:
    return \
        list(
            set(
                filter(
                    lambda it: it is not None and it != "",
                    map(
                        lambda it: str(cleaner.clean(it).lower()),
                        text.split(" ")
                    )
                )
            )
        )


def main():
    songs = ET.parse("test_songs.xml")
    out_json = {"songs": []}
    cleaner = WordCleaner()

    for child in songs.getroot().iter("song"):
        out_json["songs"].append(
            {
                "name": child.find("name").text,
                "words": extract_unique_words(cleaner, child.find("text").text)
            }
        )

    with open("processed.json", "w+") as fout:
        json.dump(out_json, fout)


if __name__ == "__main__" :
    main()
