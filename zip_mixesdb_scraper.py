from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import csv

options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

urls = [
    "https://www.mixesdb.com/w/2000-05-22_-_Zip_&_Sammy_Dee_@_Beta_Lounge,_San_Francisco",
    "https://www.mixesdb.com/w/2001-02-24_-_Zip_-_HR-XXL_Nightgroove",
    "https://www.mixesdb.com/w/2002-01-19_-_Zip_@_Dance_Under_The_Blue_Moon",
    "https://www.mixesdb.com/w/2002-05-27_-_Zip_@_PEMF,_Panacea,_Detroit",
    "https://www.mixesdb.com/w/2002-08-30_-_Richie_Hawtin,_Sammy_Dee,_Zip_@_Hotel_Pontchartrain,_Detroit",
    "https://www.mixesdb.com/w/2002-08-30_-_Zip_&_Sammy_Dee_@_The_Works,_Detroit",
    "https://www.mixesdb.com/w/2002-08-31_-_Richie_Hawtin,_Sammy_Dee,_Zip_@_Ponchartrain_Hotel,_Detroit",
    "https://www.mixesdb.com/w/2002-08-31_-_Zip_-_Paxahau_Webcast",
    "https://www.mixesdb.com/w/2004-04-17_-_Zip_@_Centre_Street,_Detroit",
    "https://www.mixesdb.com/w/2004-05-15_-_Jay_Haze,_Zip_@_Warehouse_294,_Rotterdam",
    "https://www.mixesdb.com/w/2004-05-16_-_Zip_&_Jay_Haze_@_Lofar_Afterhours,_Rotterdam",
    "https://www.mixesdb.com/w/2004-08-10_-_Zip_@_Elektrolounge,_E-Werk,_Freiburg,_Germany",
    "https://www.mixesdb.com/w/2005-02-26_-_Zip_@_Suxul_Club,_Ingolstadt,_Germany",
    "https://www.mixesdb.com/w/2005-10-29_-_Akufen,_Dimbiman_(Live_PA)_@_DEAF,_The_Village,_Dublin"
    "https://www.mixesdb.com/w/2006-01-20_-_Zip_@_Bleu,_Detroit",
    "https://www.mixesdb.com/w/2006-05-12_-_Zip_@_P3P,_K-nal,_Brussels",
    "https://www.mixesdb.com/w/2006-10-27_-_Zip_@_P3P,_K-nal,_Brussels",
    "https://www.mixesdb.com/w/2006-12-08_-_Zip_b2b_Baby_Ford_@_Get_Perlonized,_Club_NL,_Amsterdam",
    "https://www.mixesdb.com/w/2007-03-10_-_Matt_John_&_Zip_@_6_Years_Sunrise,_Bucharest",
    "https://www.mixesdb.com/w/2007-07-29_-_Zip_@_Air_Festival,_Switzerland",
    "https://www.mixesdb.com/w/2008-05-24_-_Zip_@_DEMF",
    "https://www.mixesdb.com/w/2013-05-27_-_Zip_-_Guesthouse_Live_Podcast_02",
    "https://www.mixesdb.com/w/2013-07-01_-_Zip_@_Seco_Lounge,_Tokyo",
    "https://www.mixesdb.com/w/2015-06-19_-_Zip_&_Margaret_Dygas_@_Get_Perlonized,_Poble_Espanol,_Off_Sonar"
    "https://www.mixesdb.com/w/200X_-_Raresh_%26_Zip_-_Unknown_(Uptown_Top_Sessions)",
]

def extract_tracks_from_url(url):
    print(f"▶ 読み込み中: {url}")
    driver.get(url)
    time.sleep(8)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    tracks = []

    # ✅ ページタイトルをトラックリスト名として使う
    title_tag = soup.find("h1", id="firstHeading")
    tracklist_title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if not text.startswith("["):
            continue

        text = re.sub(r"^\[[^\[\]]+\]\s*", "", text)
        label_match = re.search(r"\[([^\[\]]+)\]$", text)
        label = label_match.group(1) if label_match else ""
        text = re.sub(r"\s*\[[^\[\]]+\]$", "", text)

        if "–" in text:
            delimiter = "–"
        elif " - " in text:
            delimiter = " - "
        else:
            continue

        try:
            artist, track = map(str.strip, text.split(delimiter, 1))
            artist = re.sub(r"\[.*?\]", "", artist).strip()
            if artist and track:
                tracks.append((tracklist_title, artist, track, label, url))
        except:
            continue

    return tracks

all_tracks = []
for url in urls:
    try:
        all_tracks.extend(extract_tracks_from_url(url))
    except Exception as e:
        print(f"⚠ エラー: {url} -> {e}")

driver.quit()

# 並び替え
sorted_tracks = sorted(all_tracks, key=lambda x: (x[1].lower(), x[2].lower()))

# CSV保存
csv_path = "zip_tracklist.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Tracklist Title", "Artist", "Track", "Label", "Source URL"])
    for title, artist, track, label, source in sorted_tracks:
        writer.writerow([title, artist, track, label, source])

print(f"\n✅ CSV保存完了: {csv_path}")
