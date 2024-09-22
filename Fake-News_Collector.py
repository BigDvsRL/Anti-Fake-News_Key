import requests
from bs4 import BeautifulSoup
import time


visited = []
Real_News = ["https://www.sueddeutsche.de/", "https://www.tagesschau.de/", "https://www.spiegel.de/",
             "https://www.bbc.com/"]  # Seriöse Nachrichten
Fake_news = ["https://www.bild.de/", "https://www.nius.de/", "https://www.infowars.com"]  # FakeNews Seiten
Debunk_News = ["https://www.volksverpetzer.de/"]  # FakeNews Debunk sites

Wort_Real = set()  # bleibt unberührt!

Wort_Fake = set()  # Inhalt Wort_Fake - Wort_Real
Wort_Debunk = set()  # Inhalt (Fake_News - Wort_Real - Debunk


def clean(text):
    text = text.replace(".", " ").replace("?", " ").replace("!", "").replace(" - ", " ").replace(":", " ")
    text = text.replace('"', " ").replace("(", " ").replace(")", " ").replace("'", " ").replace(",", " ")
    text = text.replace("–", " ").replace('„', " ").replace('“', " ").replace("\n", " ").replace("»", " ")
    text = text.replace("«", " ").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    return text


def Search_URL(URL):
    crawler = set()
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    Words = set()
    a = soup.find_all("a")
    for link in a:
        if len(link.attrs) == 0:
            continue
        if "href" not in link.attrs:
            continue
        if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
            if link.attrs["href"].startswith(URL) or link.attrs["href"] == URL:
                crawler.add(link.attrs["href"])
    span = soup.find_all("span")
    for link in span:
        if len(link.attrs) == 0:
            continue
        if "href" not in link.attrs:
            continue
        if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
            if link.attrs["href"].startswith(URL) or link.attrs["href"] == URL:
                crawler.add(link.attrs["href"])

    crawler.add(URL)
    liste = soup.find_all("list")
    if len(liste) > 0:
        for link in liste.find_all("href"):
            if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
                if link.attrs["href"].startswith(URL):
                    crawler.add(link.attrs["href"])
    for site in crawler.copy():
        res = requests.get(site)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.find_all("a")
        for link in a:
            if len(link.attrs) == 0:
                continue
            if "href" not in link.attrs:
                continue
            if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
                if link.attrs["href"].startswith(URL) or link.attrs["href"] == URL:
                    if link.attrs["href"] in visited:
                        continue
                    crawler.add(link.attrs["href"])

        p = soup.find_all("p")
        if len(p) == 0:
            crawler.remove(site)
            continue
        for p_tag in p:
            if p_tag.text is None:
                continue
            text = clean(p_tag.text).split(" ")

            for t in text:
                if len(t) <= 1:
                    continue
                if not t.isnumeric():
                    Words.add(t)
    return Words


for r in Real_News:
    words = Search_URL(r)
    if words is None:
        continue
    for w in words:
        Wort_Real.add(w)
    time.sleep(2)
with open("Real_Words.txt", "w", encoding="UTF-8") as Real:
    Real.write(Wort_Real)
for f in Fake_news:
    Search_URL(f)
for d in Debunk_News:
    Search_URL(d)
