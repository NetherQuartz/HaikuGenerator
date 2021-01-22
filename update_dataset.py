"""Downloads and parses haikus by using DTF.ru API"""

import time
from bs4 import BeautifulSoup
import re
import requests
from new_haiku import punctuation_marks

if __name__ == "__main__":

    OFFSET = 0
    LOAD_BATCH = 50

    links = []
    got_len = LOAD_BATCH

    while got_len == LOAD_BATCH:
        r = requests.get("https://api.dtf.ru/v1.8/user/157777/entries",
                         headers={
                             'User-Agent': "hokku-app/1.0 (Mi Notebook Pro; Windows/10; ru; 1980x1080)",
                         },
                         params={
                             "count": str(LOAD_BATCH),
                             "offset": str(OFFSET)
                         }).json()
        links += r["result"]
        print(len(r['result']))
        got_len = len(r["result"])
        OFFSET += got_len
        time.sleep(0.4)

    print("Links exist:", len(links))

    haikus = []
    START = 0
    END = -1
    for i, e in enumerate(links[START:END]):
        print(f"\n{i + START}/{len(links)}")
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
        ERROR = str(div.text)

        div1 = div.select_one(".block-incut__text")

        div2 = div.select("div.l-island-a")

        div3 = div.select_one("div.block-quote__text")

        CHILDREN = []
        if div1 is not None:
            CHILDREN = list(div1.children)
        elif div3 is not None:
            CHILDREN = list(div3.children)
        elif len(div2) > 0:
            for c in div2:
                CHILDREN += list(c.CHILDREN)
        else:
            CHILDREN = None

        str_buf = ""

        try:
            for c in CHILDREN:
                strings = re.split(r"<br\s?/?>", str(c))
                strings = [re.sub(r"<[^<>]+>", "", s).strip() for s in strings]
                strings = list(filter(lambda x: x != "" and re.match(r"^\s*$", x) is None, strings))
                if len(strings) > 0:
                    str_buf += "\n" if str_buf != "" else ""
                    str_buf += "\n".join(strings)

            if len(str_buf.split("\n")) < 3:
                raise Exception
            haikus.append(str_buf)
            print(str_buf, "\n")
        except:
            print("ERROR:", f"{ERROR.strip()}")

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

        H = " ".join(tokens)
        print(H)
        haikus_to_write.append(H)

    with open("dataset.txt", "w", encoding="utf8") as f:
        f.write("\n".join(haikus_to_write))
