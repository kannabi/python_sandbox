import json
from typing import Set, List, Dict

import click as click

AFFIXATION = "affixation"
CONVERSION = "conversion"
COMPOSITION = "composition"
SHORTENING = "shortening"
BLENDING = "blending"
SOUND_INTERCHANGE = "sound_interchange"
SOUND_IMITATION = "sound_imitation"
BACK_FORMATION = "back_formation"
ACRONYMING = "acronyming"
TRASH = "trash"
RESET = "reset"


class ProcessingContext:
    commits: List = []
    affixation: Set[str] = set()
    conversion: Set[str] = set()
    composition: Set[str] = set()
    shortening: Set[str] = set()
    blending: Set[str] = set()
    sound_interchange: Set[str] = set()
    sound_imitation: Set[str] = set()
    back_formation: Set[str] = set()
    acronyming: Set[str] = set()


class Commit:
    def __init__(self, word: str, category: str, song_name: str):
        self.word = word
        self.category = category
        self.song_name = song_name

    def commit(self, context: ProcessingContext):
        get_set_by_category(context, self.category).add(self.word)

    def reset(self, context: ProcessingContext):
        get_set_by_category(context, self.category).remove(self.word)


def clear():
    click.clear()


def request(word: str, song_name: str):
    def ask():
        clear()
        print("affixation - 1")
        print("conversion - 2")
        print("composition - 3")
        print("shortening - 4")
        print("blending - 5")
        print("sound_interchange - 6")
        print("sound_imitation - 7")
        print("back_formation - 8")
        print("acronyming - 9")
        print("trash - 0")
        print("reset to previous - z")

        print("Song name: {}".format(song_name))
        print("Word: {}".format(word))
        answer = input("Enter category:")

        if answer == "1":
            return AFFIXATION
        if answer == "2":
            return CONVERSION
        if answer == "3":
            return COMPOSITION
        if answer == "4":
            return SHORTENING
        if answer == "5":
            return BLENDING
        if answer == "6":
            return SOUND_INTERCHANGE
        if answer == "7":
            return SOUND_IMITATION
        if answer == "8":
            return BACK_FORMATION
        if answer == "9":
            return ACRONYMING
        if answer == "0":
            return TRASH
        if answer == "z":
            return RESET
        return None

    while True:
        cmd = ask()
        if cmd is not None:
            return cmd


def backup_context(context: ProcessingContext):
    with open("context_backup.json", "w+") as backup:
        json.dump({
            "affixation": list(context.affixation),
            "conversion": list(context.conversion),
            "composition": list(context.composition),
            "shortening": list(context.shortening),
            "blending": list(context.blending),
            "sound_interchange": list(context.sound_interchange),
            "sound_imitation": list(context.sound_imitation),
            "back_formation": list(context.back_formation),
            "acronyming": list(context.acronyming),
            "commits": list(
                map(
                    lambda it: {
                        "word": it.word,
                        "category": it.category,
                        "song_name": it.song_name
                    },
                    context.commits
                )
            )
        }, backup)


def prepare_context() -> ProcessingContext:
    return ProcessingContext()


def get_set_by_category(context: ProcessingContext, cmd: str):
    if cmd == AFFIXATION:
        return context.affixation
    if cmd == CONVERSION:
        return context.conversion
    if cmd == COMPOSITION:
        return context.composition
    if cmd == SHORTENING:
        return context.shortening
    if cmd == BLENDING:
        return context.blending
    if cmd == SOUND_INTERCHANGE:
        return context.sound_interchange
    if cmd == SOUND_IMITATION:
        return context.sound_imitation
    if cmd == BACK_FORMATION:
        return context.back_formation
    if cmd == ACRONYMING:
        return context.acronyming


def main():
    context = prepare_context()
    songs: List
    with open("processed.json", "r") as fin:
        songs = json.load(fin)["songs"]

    i = 0
    j = 0

    if len(context.commits) != 0:
        last_commit = context.commits[len(context.commits) - 1]
        while True:
            song = songs[i]
            if song["name"] == last_commit.song_name:
                while True:
                    if song["words"][j] == last_commit.word:
                        break
                    j += 1
                break
            i += 1

    cmd: str
    while i < len(songs):
        song = songs[i]
        song_name = song["name"]
        words = song["words"]
        while j < len(words):
            word = words[j]
            cmd = request(word, song_name)
            commit = Commit(word, cmd, song_name)
            commit.commit(context)
            context.commits.append(commit)
            backup_context(context)
            j += 1
        i += 1


if __name__ == "__main__" :
    main()
