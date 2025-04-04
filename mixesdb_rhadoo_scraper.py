from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# ======== Rhadoo関連MixesDBリンク ========
mix_urls = [
    "https://www.mixesdb.com/w/2016-02-22_-_Rhadoo_-_Promo_Mix",
    "https://www.mixesdb.com/w/2004-03-19_-_Rhadoo%2C_Tyrant%2C_Craig_Richards_%26_Lee_Burridge_@_Studio_Martin%2C_Bucharest",
    "https://www.mixesdb.com/w/2005-03-12_-_Rhadoo_%26_Pedro_@_Escape_Club%2C_Bucharest%2C_Romania",
    "https://www.mixesdb.com/w/2006-03-26_-_Ricardo_Villalobos%2C_Rhadoo%2C_Raresh_@_Snagov_Afterparty",
    "https://www.mixesdb.com/w/2006-12-16_-_Rhadoo_@_XS_Club%2C_Iasi%2C_Romania",
    "https://www.mixesdb.com/w/2007-05-05_-_Rhadoo_@_XS_Club%2C_Iasi%2C_Romania",
    "https://www.mixesdb.com/w/2008-03-08_-_Rhadoo_%26_Raresh_@_5_Years_Kill_Your_Telly%2C_Culture_Box%2C_Copenhagen",
    "https://www.mixesdb.com/w/2008-03-23_-_Rhadoo_@_Circoloco%2C_The_End%2C_London",
    "https://www.mixesdb.com/w/2008-08-14_-_Pedro%2C_Rhadoo_%26_Dorian_Paic_@_Ibiza_Global_Radio",
    "https://www.mixesdb.com/w/2008-11-21_-_Rhadoo_@_In_Tenisi%2C_Club_Mash-Up%2C_Bucharest",
    "https://www.mixesdb.com/w/2010_-_Rhadoo_@_El_CZR_Birthday_Party",
    "https://www.mixesdb.com/w/2010-03-13_-_VA_@_9_Years_Of_Sunrise%2C_Kristal_Glam_Club%2C_Romania",
    "https://www.mixesdb.com/w/2010-05-28_-_Raresh_%26_Rhadoo_@_12_Hours_Dance_Marathon%2C_Ciric_Lake%2C_Romania",
    "https://www.mixesdb.com/w/2010-10-09_-_Don_Juanito_%26_Nima_Gorji_%26_Rhadoo_@_Ibiza_Underground_Closing_Party",
    "https://www.mixesdb.com/w/2010-11-24_-_Taimur_Agha%2C_Rhadoo_@_Halcyon_The_Shop%2C_NYC_(The_Bandwagon_Podcast_027)",
    "https://www.mixesdb.com/w/2012-04-14_-_Rhadoo_@_Lessizmore%2C_Fuse%2C_Brussels",
    "https://www.mixesdb.com/w/2012-08-18_-_Rhadoo_@_Sunwaves_12%2C_Romania",
    "https://www.mixesdb.com/w/2012-10-27_-_Rhadoo_@_Halloween_Labyrinth%2C_Arma17%2C_Moscow_(Arma_Podcast_078)",
    "https://www.mixesdb.com/w/2013-01-06_-_Rhadoo_@_La_Santanera%2C_The_BPM_Festival%2C_Mexico",
    "https://www.mixesdb.com/w/2013-05-05_-_Rhadoo_b2b_Ricardo_Villalobos_@_Sunwaves_13%2C_Romania",
    "https://www.mixesdb.com/w/2013-07-20_-_Rhadoo_@_Fabric%2C_London",
    "https://www.mixesdb.com/w/2013-11-02_-_Rhadoo_@_11_Yr_Anniversary%2C_Arma17%2C_Moscow",
    "https://www.mixesdb.com/w/2014-03-13_-_Rhadoo_@_Dommune%2C_Tokyo",
    "https://www.mixesdb.com/w/2015-05-01_-_Rhadoo_@_Sunwaves_17%2C_Mamaia%2C_Romania",
    "https://www.mixesdb.com/w/2016-08-11_-_Rhadoo_@_Sunwaves_20%2C_Romania",
    "https://www.mixesdb.com/w/2017-03-31_-_Rhadoo_@_Dommune%2C_Tokyo",
    "https://www.mixesdb.com/w/2018-10-20_-_Rhadoo_@_19_Years_Fabric%2C_London_(GH001)",
    "https://www.mixesdb.com/w/2019-11-01_-_Rhadoo_@_Mutabor%2C_Moscow_(the_Volks_Podcast_020)",
    "https://www.mixesdb.com/w/2019-11-22_-_Rhadoo_@_Super_Dommune%2C_Tokyo",
    "https://www.mixesdb.com/w/2020-12-15_-_Rhadoo_@_Sunwaves_Virtual_Festival",
    "https://www.mixesdb.com/w/2021-04-30_-_Rhadoo_@_Sunwaves_27%2C_Mamaia%2C_Romania",
]

# ======== Chromeドライバ設定 ========
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

data = []

for url in mix_urls:
    driver.get(url)
    time.sleep(5)  # Cloudflare突破待ち

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # ミックスタイトル取得
        mix_title = soup.select_one("h1.firstHeading").text.strip()

        # 🎯 正しいセレクタでトラック取得（div.list-track）
        tracks = [div.text.strip() for div in soup.select("div.list-track") if div.text.strip()]

        # fallback：万が一構造が違った場合
        if not tracks:
            tracks = [li.text.strip() for li in soup.select("div.mw-parser-output li") if li.text.strip()]

        for track in tracks:
            data.append({"Mix Title": mix_title, "Track": track, "URL": url})

        print(f"✅ {mix_title} - {len(tracks)} tracks")
    except Exception as e:
        print(f"❌ Failed to parse {url}: {e}")

driver.quit()

# ======== CSV保存 ========
df = pd.DataFrame(data)
df.to_csv("mixesdb_rhadoo_tracklists_v2.csv", index=False)
print("✅ Saved to mixesdb_rhadoo_tracklists_v2.csv")