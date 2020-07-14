from numpy import random
from re import sub


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


data = open("sample.txt", encoding="utf8").read()

strings = data.split('\n')

d = {}
all_words = []
for s in strings:
    words = list(filter(lambda x: x.isalpha(), map(lambda x: x.lower(), s.split(' '))))
    words = list(map(lambda x: sub("ё", "е", x), words))
    pair = make_pairs(words)
    for w1, w2 in pair:
        if w1 in d.keys():
            d[w1].append(w2)
        else:
            d[w1] = [w2]
    all_words += words

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

print(" ".join(F))
print(" ".join(S))
print(" ".join(T))
