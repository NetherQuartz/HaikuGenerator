from numpy import random
from re import sub
from string import punctuation
from typing import List

punctuation_marks = list(punctuation) + ["...", "!!!", "«", "»"]
terminal_marks = ["...", "!!!", ".", "!", "?"]

vowels = ['а', 'е', 'и', 'о', 'у', 'ы', 'ю', 'я']


def make_pairs(w: list):
    """Generates pairs of words from list following each other

    :param w: list of words
    """
    for i in range(len(w) - 1):
        yield w[i], w[i + 1]


def count_vowels(w: str) -> int:
    """Returns number of vowels in a given string

    :param w: string
    :return: number of vowels
    """
    v = 0
    for c in w:
        if c in vowels:
            v += 1
    return v


def next_word(d: dict, previous: str) -> (bool, str):
    """Returns next word in Markov chain

    :param d: dictionary of words
    :param previous: previous word in chain
    :return: True and next word in chain if it can be found, else False and empty string
    """
    if previous not in d.keys() or len(d[previous]) == 0:
        return False, ""
    prob = []
    for p in d[previous]:
        prob.append(p)
    if len(prob) > 0:
        return True, random.choice(prob)[:]
    else:
        return False, ""


def normalize_punctuation(haiku: List[List[str]]) -> List[List[str]]:
    """Removes punctuation marks in beginning of rows and moves them to the end of
    previous row if it exists. Edits input list too, so make sure that you've copied it.

    :param haiku: list of haiku rows e.g. lists containing strings
    :return: edited input
    """
    for i in range(len(haiku)):
        if haiku[i][0] in punctuation_marks:
            if i > 0:
                haiku[i - 1].append(haiku[i][0])
            haiku[i].pop(0)
    return haiku


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


def put_capital(haiku: List[List[str]]) -> List[List[str]]:
    """Capitalize first words in a row and words that are in the end of sentence.
    Edits input list too, so make sure that you've copied it.

    :param haiku: list of haiku rows e.g. lists containing strings
    :return: edited input
    """
    for row in haiku:
        for i in range(len(row)):
            if i == 0 or i - 1 > 0 and row[i - 1] in terminal_marks:
                row[i] = row[i].capitalize()
    return haiku


if __name__ == "__main__":

    with open("sample.txt", encoding="utf8") as file:
        data = file.read()

    strings = data.split('\n')

    chain = {}
    for s in strings:
        words = list(filter(lambda x: True, map(lambda x: x.lower(), s.split(' '))))
        words = list(map(lambda x: sub("ё", "е", x), words))
        pair = make_pairs(words)
        for w1, w2 in pair:
            if w1 in chain.keys():
                chain[w1].append(w2)
            else:
                chain[w1] = [w2]

    F, S, T = [], [], []
    while count_vowels(" ".join(F + S + T)) != 5 + 7 + 5:
        F, S, T = [], [], []
        prev = random.choice(list(chain.keys()))
        for l, n in [(F, 5), (S, 7), (T, 5)]:
            r, s = next_word(chain, prev)
            while r and count_vowels(" ".join(l)) < n:
                l.append(s)
                r, s = next_word(chain, s)
            if len(l) > 0:
                prev = l[-1]
            else:
                break
        if count_vowels(" ".join(F)) != 5 or count_vowels(" ".join(S)) != 7 or count_vowels(" ".join(T)) != 5:
            continue

    l = normalize_punctuation([F, S, T])
    l = put_capital(l)
    for s in l:
        print(" ".join(join_punctuation(s)))
