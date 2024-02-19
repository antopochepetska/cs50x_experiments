import argparse
from pathlib import Path
from datetime import datetime
import time
import re

N = 26
WORDS_COUNT = 0

class Node:
    def __init__(self, element):
        self.element = element
        self.next = 0

hash_table = [None] * N

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

def check(word_from_text: str) -> bool:
    """Returns true if word is in dictionary, else false"""
    row = hash(word)
    current = hash_table[row]
    while current:
        if current.element == word_from_text:
            return True
        else:
            current = current.next
    return False


def hash(word: str) -> int:
    """Hashes word to a number"""
    return ord(word[0].upper()) - 65


def load(dict_file) -> bool:
    """Loads dictionary into memory, returning true if successful, else false"""
    with open(dict_file, 'r') as f:
        while line  := f.readline():
            word = line.strip("\n")

            new_word = Node(word)
            global WORDS_COUNT
            WORDS_COUNT += 1
            row = hash(word)

            if hash_table[row] is None:
                hash_table[row] = new_word
                new_word.next = None
            else:
                new_word.next = hash_table[row]
                hash_table[row] = new_word



if __name__ == '__main__':

    startTime = time.time()

    words_dict = dict()
    misspelled_words = list()

    start = time.time()
    start_dict_load = time.time()
    load(dict_file)
    end_dict_load = time.time()

    with open(text, 'r') as f:
        text_to_check = f.read()

    text_to_check = text_to_check.replace(",", " ")
    text_to_check = text_to_check.replace(".", " ")
    text_to_check = " ".join(text_to_check.split())
    for word in text_to_check.split():
        word = word.strip("!").strip("?").strip("(").strip(")").strip(";").strip(":")
        # print(f"WORD {word}")
        if eligible(word) and not check(word.lower()):
            misspelled_words.append(word)

    done = time.time()

    print(f"MISSPELLED WORDS: {misspelled_words}")
    print(f"WORDS MISSPELLED: {len(misspelled_words)}")
    print(f"WORDS IN DICTIONARY: {WORDS_COUNT}")
    print(f"WORDS IN TEXT: {len(text_to_check.split())}")

    print(f"TIME IN load: {end_dict_load - start_dict_load}")
    print(f"TIME IN TOTAL: {done - startTime}")
