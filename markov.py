from numpy import random
from re import sub
from string import punctuation
from typing import List


def make_pairs(w: list):
    for i in range(len(w) - 1):
        yield w[i], w[i + 1]


def count_vowels(w: str) -> int:
    vowels = ['а', 'е', 'и', 'о', 'у', 'ы', 'ю', 'я']
    v = 0
    for c in w:
        if c in vowels:
            v += 1
    return v


def next_word(d: dict, src: str):
    if src not in d.keys() or len(d[src]) == 0:
        return False, ""
    prob = []
    for p in d[src]:
        prob.append(p)
    if len(prob) > 0:
        return True, random.choice(prob)[:]
    else:
        return False, ""


def normalize_punctuation(l: List[List[str]]) -> List[List[str]]:
    for i in range(len(l)):
        if l[i][0] in punctuation:
            if i > 0:
                l[i - 1].append(l[i][0])
            l[i].pop(0)
    return l


def join_punctuation(l: List[str]) -> List[str]:
    l = l[:]
    i = 0
    while i < len(l):
        if l[i] in punctuation:
            l[i - 1] += l[i]
            l.pop(i)
        else:
            i += 1
    return l

data = open("sample.txt", encoding="utf8").read()

strings = data.split('\n')

d = {}
for s in strings:
    words = list(filter(lambda x: True, map(lambda x: x.lower(), s.split(' '))))
    words = list(map(lambda x: sub("ё", "е", x), words))
    pair = make_pairs(words)
    for w1, w2 in pair:
        if w1 in d.keys():
            d[w1].append(w2)
        else:
            d[w1] = [w2]

F, S, T = [], [], []
while count_vowels(" ".join(F + S + T)) != 5 + 7 + 5:
    F, S, T = [], [], []
    prev = random.choice(list(d.keys()))
    for l, n in [(F, 5), (S, 7), (T, 5)]:
        r, s = next_word(d, prev)
        while r and count_vowels(" ".join(l)) < n:
            l.append(s)
            r, s = next_word(d, s)
        if len(l) > 0:
            prev = l[-1]
        else:
            break
    if count_vowels(" ".join(F)) != 5 or count_vowels(" ".join(S)) != 7 or count_vowels(" ".join(T)) != 5:
        continue

l = normalize_punctuation([F, S, T])
for s in l:
    print(" ".join(join_punctuation(s)))
