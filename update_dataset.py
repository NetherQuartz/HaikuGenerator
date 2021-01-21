import requests
import time
from bs4 import BeautifulSoup
import re

from new_haiku import punctuation_marks

links = []
offset = 0
load_batch = 50
got_len = load_batch

while got_len == load_batch:
    r = requests.get("https://api.dtf.ru/v1.8/user/157777/entries",
                     headers={
                         'User-Agent': "hokku-app/1.0 (Mi Notebook Pro; Windows/10; ru; 1980x1080)",
                     },
                     params={
                         "count": str(load_batch),
                         "offset": str(offset)
                     }).json()
    links += r["result"]
    print(len(r['result']))
    got_len = len(r["result"])
    offset += got_len
    time.sleep(0.4)

print("Links exist:", len(links))

haikus = []
start = 0
end = -1
for i, e in enumerate(links[start:end]):
    print(f"\n{i + start}/{len(links)}")
    r = requests.get("https://api.dtf.ru/v1.8/entry/locate",
                     headers={
                         'User-Agent': "hokku-app/1.0 (Mi Notebook Pro; Windows/10; ru; 1980x1080)",
                     },
                     params={
                         "url": e["url"]
                     }).json()
    html = r["result"]["entryContent"]["html"]
    soup = BeautifulSoup(html, 'lxml')
    div = soup.select_one("div.content")
    er = str(div.text)

    div1 = div.select_one(".block-incut__text")

    div2 = div.select("div.l-island-a")

    div3 = div.select_one("div.block-quote__text")

    children = []
    if div1 is not None:
        children = list(div1.children)
    elif div3 is not None:
        children = list(div3.children)
    elif len(div2) > 0:
        for c in div2:
            children += list(c.children)
    else:
        children = None

    st = ""

    try:
        for c in children:
            strings = re.split(r"<br\s?/?>", str(c))
            strings = [re.sub(r"<[^<>]+>", "", s).strip() for s in strings]
            strings = list(filter(lambda x: x != "" and re.match(r"^\s*$", x) is None, strings))
            if len(strings) > 0:
                st += "\n" if st != "" else ""
                st += "\n".join(strings)

        if len(st.split("\n")) < 3:
            raise Exception
        haikus.append(st)
        print(st, "\n")
    except:
        print("ERROR:", f"{er.strip()}")

    time.sleep(0.4)

print(f"Without errors: {len(haikus)}/{len(links)}")

haikus_to_write = []

for haiku in haikus:
    tokens = []
    for line in haiku.split("\n"):
        for word in line.split():
            while len(word) > 0 and word[:3] in punctuation_marks:
                tokens.append(word[:3])
                word = word[3:]
            while len(word) > 0 and word[0] in punctuation_marks:
                tokens.append(word[0])
                word = word[1:]
            found_word = re.findall(r"(\w+(-\w+)?)", word)
            if len(found_word) > 0:
                tokens.append(found_word[0][0])
                word = re.sub(r"(\w+(-\w+)?)", "", word)
            while len(word) > 0 and word[0] in punctuation_marks:
                if word[:3] in punctuation_marks:
                    tokens.append(word[:3])
                    word = word[3:]
                else:
                    tokens.append(word[0])
                    word = word[1:]

    h = " ".join(tokens)
    print(h)
    haikus_to_write.append(h)

with open("dataset.txt", "w", encoding="utf8") as f:
    f.write("\n".join(haikus_to_write))
