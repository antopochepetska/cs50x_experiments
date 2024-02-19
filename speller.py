import argparse
from pathlib import Path
from datetime import datetime
import time
import re


parser = argparse.ArgumentParser()
parser.add_argument("dict_path")
parser.add_argument("file_path")

args = parser.parse_args()
dict_file = Path(args.dict_path)
text = Path(args.file_path)

if not dict_file.exists():
    print("This dictionary does not exist")
    raise SystemExit(1)

if not text.exists():
    print("This text file does not exist")
    raise SystemExit(1)


def eligible(word: str) -> bool:
    if len(word) > 45 or word.startswith("'"):
        return False
    if any(i.isdigit() for i in word):
        return False
    if word.isalpha():
        return True
    return False


if __name__ == '__main__':

    startTime = time.time()

    words_dict = dict()
    misspelled_words = list()

    start = time.time()
    start_dict_load = time.time()
    with open(dict_file, 'r') as f:
        while line  := f.readline():
            words_dict[line.strip("\n")] = 1
    end_dict_load = time.time()

    with open(text, 'r') as f:
        text_to_check = f.read()

    text_to_check = text_to_check.replace(",", " ")
    text_to_check = text_to_check.replace(".", " ")
    text_to_check = " ".join(text_to_check.split())
    for word in text_to_check.split():
        word = word.strip("!").strip("?").strip("(").strip(")").strip(";").strip(":")
        # print(f"WORD {word}")
        if eligible(word):
            if words_dict.get(word.lower()) is None:
                misspelled_words.append(word)

    done = time.time()

    print(f"MISSPELLED WORDS: {misspelled_words}")
    print(f"WORDS MISSPELLED: {len(misspelled_words)}")
    print(f"WORDS IN DICTIONARY: {len(words_dict)}")
    print(f"WORDS IN TEXT: {len(text_to_check.split())}")

    print(f"TIME IN load: {end_dict_load - start_dict_load}")
    print(f"TIME IN TOTAL: {done - startTime}")
