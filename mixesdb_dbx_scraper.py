from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Daniel Bell全ミックスURL（自動取得済み）
mix_urls = [
    "https://www.mixesdb.com/w/2001-02-02_-_Daniel_Bell_-_La_Boum_Deluxe",
    "https://www.mixesdb.com/w/2001-02-03_-_Daniel_Bell_@_Flex,_Vienna",
    "https://www.mixesdb.com/w/2001-06-23_-_Daniel_Bell_@_Detroit-Starclub,_Globus,_Berlin",
    "https://www.mixesdb.com/w/2001-12-01_-_Pole,_Barbara_Preisinger,_Daniel_Bell,_Sven_VT_@_Scape_Night,_WMF,_Berlin",
    "https://www.mixesdb.com/w/2002-02-01_-_Daniel_Bell_@_Radio_Radiostacja",
    "https://www.mixesdb.com/w/2003-02-27_-_Daniel_Bell_vs_Cabanne_-_Novamix",
    "https://www.mixesdb.com/w/2003-03-15_-_Daniel_Bell_@_12_Years_Tresor,_Berlin",
    "https://www.mixesdb.com/w/2003-04-20_-_Daniel_Bell_@_Digital_Gadget",
    "https://www.mixesdb.com/w/2003-11-15_-_Martin_Landsky,_Daniel_Bell_@_Harpune,_D%C3%BCsseldorf",
    "https://www.mixesdb.com/w/2004-03-13_-_Daniel_Bell_@_13_Years_Tresor,_Berlin",
    "https://www.mixesdb.com/w/2004-03-13_-_Daniel_Bell_@_Dance_Under_The_Blue_Moon",
    "https://www.mixesdb.com/w/2004-06-10_-_Daniel_Bell,_Dave_Turov_@_WMF_im_Caf%C3%A9_Moskau,_Berlin",
    "https://www.mixesdb.com/w/2004-06-19_-_Daniel_Bell_@_WMF_im_Caf%C3%A9_Moskau,_Berlin",
    "https://www.mixesdb.com/w/2005-05-30_-_Daniel_Bell_@_Underground_Stage,_Fuse-In,_Detroit",
    "https://www.mixesdb.com/w/2005-07-02_-_Daniel_Bell_@_Distillery,_Leipzig",
    "https://www.mixesdb.com/w/2005-12-10_-_Daniel_Bell_@_Avalon",
    "https://www.mixesdb.com/w/2005_-_Daniel_Bell_@_Distillery,_Leipzig,_02-07-2005",
    "https://www.mixesdb.com/w/2006-01-20_-_Daniel_Bell_@_Blue_Room,_Detroit",
    "https://www.mixesdb.com/w/2006-03-13_-_Daniel_Bell_@_Icomplex,_Los_Angeles",
    "https://www.mixesdb.com/w/2006-06-30_-_Daniel_Bell_@_Pacotek,_Tel-Aviv,_Jerusalem",
    "https://www.mixesdb.com/w/2006-09-30_-_Daniel_Bell_@_Coliseum_-_Charleroi",
    "https://www.mixesdb.com/w/2006-12-30_-_Daniel_Bell_@_Substatic_Club",
    "https://www.mixesdb.com/w/2007-06-23_-_Daniel_Bell_@_Silo_Club,_Leuven,_Warm_FM",
    "https://www.mixesdb.com/w/2007-07-28_-_Daniel_Bell,_Jay_Denham,_Beatnik_@_Rote_Sonne_Club,_Munich",
    "https://www.mixesdb.com/w/2007-11-24_-_Daniel_Bell_@_STRP_Festival,_Eindhoven",
    "https://www.mixesdb.com/w/2007-11-25_-_Daniel_Bell_@_Tresor,_Berlin",
    "https://www.mixesdb.com/w/2008-03-15_-_Daniel_Bell,_Serafin_@_Hidden_Club,_Switzerland",
    "https://www.mixesdb.com/w/2008-03-23_-_Daniel_Bell_@_Awakenings_-_Easter_Anniversary",
    "https://www.mixesdb.com/w/2008-04-11_-_Daniel_Bell_@_The_Bunker,_NYC_(TBP_12,_2008-04-23)",
    "https://www.mixesdb.com/w/2009-02-28_-_Daniel_Bell,_Electric_Lane_@_2_Years_The_Villa,_Oslo",
    "https://www.mixesdb.com/w/2010-01-14_-_Daniel_Bell_@_RTS.FM_Studio,_Berlin",
    "https://www.mixesdb.com/w/2013-05-26_-_Daniel_Bell_@_Movement,_Detroit",
    "https://www.mixesdb.com/w/2013-05-26_-_Daniel_Bell_@_Movement,_Detroit_(Boiler_Room)",
    "https://www.mixesdb.com/w/2014-01-11_-_Daniel_Bell_@_Superpleasures,_Fusion_Beach_Club,_The_BPM_Festival,_Mexico",
    "https://www.mixesdb.com/w/2014-11-28_-_Daniel_Bell_@_Episode_10,_Closer,_Kiev",
    "https://www.mixesdb.com/w/2015-05-03_-_Daniel_Bell_@_A_Detroit_Affair,_Studio_338,_London",
    "https://www.mixesdb.com/w/2015-10-17_-_Daniel_Bell_@_ReSolute,_NYC",
    "https://www.mixesdb.com/w/2016-07-20_-_Daniel_Bell_-_XLR8R_Podcast_448",
    "https://www.mixesdb.com/w/2017-01-12_-_Daniel_Bell_@_Detroit_Love,_Canibal_Royal,_The_BPM_Festival,_Mexico",
    "https://www.mixesdb.com/w/2018-02-03_-_Daniel_Bell_@_Yoyaku_Instore_Session"
]

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

data = []

for url in mix_urls:
    driver.get(url)
    time.sleep(5)

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        mix_title = soup.select_one("h1.firstHeading").text.strip()

        tracks = [div.text.strip() for div in soup.select("div.list-track") if div.text.strip()]
        if not tracks:
            tracks = [li.text.strip() for li in soup.select("div.mw-parser-output li") if li.text.strip()]

        for track in tracks:
            data.append({"Mix Title": mix_title, "Track": track, "URL": url})

        print(f"✅ {mix_title} - {len(tracks)} tracks")
    except Exception as e:
        print(f"❌ Failed to parse {url}: {e}")

driver.quit()

df = pd.DataFrame(data)
df.to_csv("mixesdb_danielbell_tracklists.csv", index=False)
print("✅ Saved to mixesdb_danielbell_tracklists.csv")
