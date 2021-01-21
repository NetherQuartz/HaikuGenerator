import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup
import re

l = []
off = 0
count = 50
while off < 300:
    r = requests.get("https://api.dtf.ru/v1.8/user/157777/entries",
                     headers={
                         'User-Agent': "hokku-app/1.0 (Mi Notebook Pro; Windows/10; ru; 1980x1080)",
                     },
                     params={
                         "count": str(count),
                         "offset": str(off)
                     }).json()
    l += r["result"]
    off += count
    time.sleep(0.4)

posts = []
texts = []
for e in l:
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
    try:
        soup.select_one("textarea").decompose()
    except:
        pass
    div.select_one("div.l-island-a").decompose()

    pat = r"([A-Za-zа-яА-Я0-9ёЁ.,\-\":?!—]+)"

    texts.append(" ".join(re.findall(pat, div.text)))
    posts.append(div.text)

    time.sleep(0.4)

pprint(texts)
f = open("posts.txt", 'w', encoding="utf8")
f.write("\n".join(posts))
f.close()
f = open("texts.txt", 'w', encoding="utf8")
f.write("\n".join(texts))
f.close()
