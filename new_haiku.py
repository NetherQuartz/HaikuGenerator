"""Generates haikus by using Markov chain"""

from re import sub
from string import punctuation
from typing import List
from numpy import random

punctuation_marks = list(punctuation) + ["...", "!!!", "«", "»", "—"]
terminal_marks = ["...", "!!!", ".", "!", "?"]

vowels = ['а', 'е', 'и', 'о', 'у', 'ы', 'ю', 'я']


def make_pairs(word_list: list):
    """Generates pairs of words from list following each other

    :param word_list: list of words
    """
    for i in range(len(word_list) - 1):
        yield word_list[i], word_list[i + 1]


def count_vowels(row: List[str]) -> int:
    """Returns number of vowels in a given haiku row

    :param row: haiku row i.e. list of strings
    :return: number of vowels
    """
    row_s = " ".join(row)
    vowels_count = 0
    for char in row_s:
        if char in vowels:
            vowels_count += 1
    return vowels_count


def next_word(word_dict: dict, previous: str) -> (bool, str):
    """Returns next word in Markov chain

    :param word_dict: dictionary of words
    :param previous: previous word in chain
    :return: True and next word in chain if it can be found, else False and empty string
    """
    if previous not in word_dict.keys() or len(word_dict[previous]) == 0:
        return False, ""
    prob = []
    for word in word_dict[previous]:
        prob.append(word)
    if len(prob) > 0:
        return True, random.choice(prob)[:]
    return False, ""


def normalize_punctuation(haiku_rows: List[List[str]]) -> List[List[str]]:
    """Removes punctuation marks in beginning of rows and moves them to the end of
    previous row if it exists. Edits input list too, so make sure that you've copied it.

    :param haiku_rows: list of haiku rows e.g. lists containing strings
    :return: edited input
    """
    for i, row in enumerate(haiku_rows):
        if row[0] in punctuation_marks:
            if i > 0:
                haiku_rows[i - 1].append(row[0])
            row.pop(0)
    return haiku_rows


def join_punctuation(row: List[str]) -> List[str]:
    """Concatenates punctuation marks to previous word and removes quotes and braces.

    :param row: haiku row e.g. list containing strings
    :return: edited input
    """
    row = row[:]
    i = 0
    while i < len(row):
        if row[i] in punctuation_marks:
            if row[i] in ['"', '«', '»', '(', ')'] or \
                    (i > 0 and row[i - 1][-1] in punctuation_marks):
                row.pop(i)
                continue
            if row[i] == '-':
                row[i - 1] += ' '
            row[i - 1] += row[i]
            row.pop(i)
        else:
            i += 1
    return row


def put_capital(haiku_rows: List[List[str]]) -> List[List[str]]:
    """Capitalize first words in a row and words that are in the end of sentence.
    Edits input list too, so make sure that you've copied it.

    :param haiku_rows: list of haiku rows e.g. lists containing strings
    :return: edited input
    """
    for row in haiku_rows:
        for i, word in enumerate(row):
            if i == 0 or i - 1 > 0 and row[i - 1] in terminal_marks:
                row[i] = word.capitalize()
    return haiku_rows


if __name__ == "__main__":

    with open("dataset.txt", encoding="utf8") as file:
        data = file.read()

    strings = data.split('\n')  # get list of lines from file

    chain = {}
    for s in strings:
        words = list(map(lambda x: x.lower(), s.split(' ')))
        words = list(map(lambda x: sub("ё", "е", x), words))
        pair = make_pairs(words)
        for w1, w2 in pair:
            if w1 in chain.keys():
                chain[w1].append(w2)
            else:
                chain[w1] = [w2]

    F, S, T = [], [], []  # first, second and third rows of haiku
    while count_vowels(F) != 5 or count_vowels(S) != 7 or count_vowels(T) != 5:
        F, S, T = [], [], []
        prev = random.choice(list(chain.keys()))
        for l, n in [(F, 5), (S, 7), (T, 5)]:
            r, s = next_word(chain, prev)
            while r and count_vowels(l) < n:
                l.append(s)
                r, s = next_word(chain, s)
            if len(l) > 0:
                prev = l[-1]
            else:
                break

    haiku = put_capital(normalize_punctuation([F, S, T]))
    for s in haiku:
        print(" ".join(join_punctuation(s)))
