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


def save():
    with open("Real_Words.txt", "w", encoding="UTF-8") as Real:
        for i in Wort_Real:
            Real.write(str(Wort_Real + "\n"))
    with open("Fake_Words.txt", "w", encoding="UTF-8") as Fake:
        for i in Wort_Fake:
            Real.write(str(Wort_Fake + "\n"))
        Fake.write(str(Wort_Fake))
    with open("Debunk_Words.txt", "w", encoding="UTF-8") as Bunk:
        for i in Wort_Debunk:
            Real.write(str(Wort_Debunk + "\n"))
        Bunk.write(str(Wort_Debunk))


def load_Words():
    try:
        with open("Real_Words.txt", "r") as Real:
            for i in Real:
                i = i.replace("\n")
                Wort_Real.add(i)
            pass
        with open("Fake_Words.txt", "r") as Fake:
            for i in Fake:
                i = i.replace("\n")
                Wort_Fake.add(i)
            pass
        with open("Debunk_Words.txt", "r") as Debunk:
            for i in Debunk:
                i = i.replace("\n")
                Wort_Debunk.add(i)
            pass
    except:
        return
    for Item in Wort_Real:
        if Item in Wort_Fake:
            Wort_Fake.remove(Item)
        if Item in Wort_Debunk:
            Wort_Debunk.remove(Item)
    for F_Item in Wort_Fake:
        if F_Item in Wort_Debunk:
            Wort_Debunk.remove(F_Item)
    save()

def clean(text):
    text = text.replace(".", " ").replace("?", " ").replace("!", "").replace(" - ", " ").replace(":", " ")
    text = text.replace('"', " ").replace("(", " ").replace(")", " ").replace("'", " ").replace(",", " ")
    text = text.replace("–", " ").replace('„', " ").replace('“', " ").replace("\n", " ").replace("»", " ")
    text = text.replace("«", " ").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    return text


def load_whisper():
    # installs Whisper
    import subprocess
    subprocess.run("pip install git+https://github.com/openai/whisper.git")
    time.sleep(20)


def Video_to_Text(Videopath):
    # Load OpenAI Whisper
    try:
        import whisper
        from subprocess import call
        pass
    except ImportError:
        load_whisper()
        while True:
            try:
                import whisper
                break
            except ImportError:
                time.sleep(5)
    model = whisper.load_model("base")
    filename, ext = os.path.splitext(Videopath)
    # Turning Video into Audio without Saving!
    audio = subprocess.call(["ffmpeg", "-y", "-i", Videopath, f"{filename}.{'wav'}"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
    result = model.transcribe(Video_to_Text)
    # load Video into Whisper and return String without Timestamp


def Search_URL(URL):
    crawler = set()
    try:
        res = requests.get(URL)
    except requests.SSLError:
        return None
    except requests.ConnectionError:
        requests.history = 0
        pass
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
        if link.attrs["href"].startswith("/") and (
                not link.attrs["href"].startswith("http") or not link.attrs["href"].startswith("www")):
            li = str(URL) + link.attrs["href"][1:]
            crawler.add(li)

    span = soup.find_all("span")
    for link in span:
        if len(link.attrs) == 0:
            continue
        if "href" not in link.attrs:
            continue
        if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
            if link.attrs["href"].startswith(URL) or link.attrs["href"] == URL:
                crawler.add(link.attrs["href"])
            if link.attrs["href"].startswith("/") and (
                    not link.attrs["href"].startswith("http") or not link.attrs["href"].startswith("www")):
                li = str(URL) + link.attrs["href"][1:]
                crawler.add(li)

    div = soup.find_all("div")
    # DIV Kein Link in HREF
    # Link in A
    for link in div:
        if len(link.attrs) == 0:
            continue
        if "href" not in link.attrs:
            continue
        if link.attrs["href"].startswith("http") or link.attrs["href"].startswith("www"):
            if link.attrs["href"].startswith(URL) or link.attrs["href"] == URL:
                crawler.add(link.attrs["href"])
            if link.attrs["href"].startswith("/") and (
                    not link.attrs["href"].startswith("http") or not link.attrs["href"].startswith("www")):
                li = str(URL) + link.attrs["href"][1:]
                crawler.add(li)

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

        div = soup.find_all("div")
        if len(div) == 0:
            crawler.remove(site)
            continue
        for div_tag in div:
            if div_tag.text is None:
                continue
            text = clean(div_tag.text).split(" ")

            for t in text:
                if len(t) <= 1:
                    continue
                if len(t.split("/")) > 1 or len(t.split("=")) > 1:
                    continue
                if not t.isnumeric() and not t[0:2].isnumeric():
                    # Filter out ASCII Signs
                    Words.add(t)

        h2 = soup.find_all("h2")
        if len(h2) == 0:
            crawler.remove(site)
            continue
        for h2_tag in h2:
            if h2_tag.text is None:
                continue
            text = clean(h2_tag.text).split(" ")
            for t in text:
                if len(t) <= 1:
                    continue
                if len(t.split("/")) > 1 or len(t.split("=")) > 1:
                    continue
                if not t.isnumeric() and not t[0:2].isnumeric():
                    # Filter out ASCII Signs
                    Words.add(t)

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
                if len(t.split("/")) > 1 or len(t.split("=")) > 1:
                    continue
                if not t.isnumeric() and not t[0:2].isnumeric():
                    # Filter out ASCII Signs
                    Words.add(t)
    return Words


if __name__ == "main":
    pass
    for r in Real_News:
        words = None
        words = Search_URL(r)
        if words is None:
            continue
        for w in words:
            Wort_Real.add(w)
        time.sleep(2)
    if len(Wort_Real) > 0:
        with open("Real_Words.txt", "w", encoding="UTF-8") as Real:
            for i in Wort_Real:
                Real.write(str(Wort_Real + "\n"))

    for f in Fake_news:
        words = None
        try:
            pass
            words = Search_URL(f)
        except Exception as e:
            print(e)
            continue
        if words is None:
            continue
        for w in words:
            Wort_Fake.add(w)
        time.sleep(2)
    with open("Fake_Words.txt", "w", encoding="UTF-8") as Fake:
        for i in Wort_Fake:
            Real.write(str(Wort_Fake + "\n"))
        Fake.write(str(Wort_Fake))

    for d in Debunk_News:
        words = None
        try:
            words = Search_URL(d)
        except Exception as e:
            print(e)
            continue
        if words is None:
            continue
        for w in words:
            Wort_Debunk.add(w)
        time.sleep(2)
    with open("Debunk_Words.txt", "w", encoding="UTF-8") as Bunk:
        for i in Wort_Debunk:
            Real.write(str(Wort_Debunk + "\n"))
        Bunk.write(str(Wort_Debunk))
