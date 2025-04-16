import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# ==============================
# STEP 1: 全URLを取得（ページ分割対応）
# ==============================

def get_mix_urls():
    base_url = "https://www.mixesdb.com"
    start_url = "/w/Category:Zip"
    full_links = []

    while start_url:
        url = base_url + start_url
        print(f"🔍 Scanning: {url}")
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        links = [
            base_url + a["href"]
            for a in soup.find_all("a", href=True)
            if a["href"].startswith("/w/20")
        ]
        full_links.extend(links)

        next_link = soup.find("a", string="next page")
        start_url = next_link["href"] if next_link else None

    return sorted(set(full_links))

# ==============================
# STEP 2: 各ページからトラックリストを抽出
# ==============================

def scrape_tracklists(mix_urls):
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

            # div.list-track or li fallback
            tracks = [div.text.strip() for div in soup.select("div.list-track") if div.text.strip()]
            if not tracks:
                tracks = [li.text.strip() for li in soup.select("div.mw-parser-output li") if li.text.strip()]

            for track in tracks:
                data.append({
                    "Mix Title": mix_title,
                    "Track": track,
                    "URL": url
                })

            print(f"✅ {mix_title} - {len(tracks)} tracks")

        except Exception as e:
            print(f"❌ Failed to parse {url}: {e}")

    driver.quit()
    return data

# ==============================
# MAIN処理
# ==============================

if __name__ == "__main__":
    urls = get_mix_urls()
    results = scrape_tracklists(urls)

    df = pd.DataFrame(results)
    df.to_csv("mixesdb_danielbell_tracklists.csv", index=False)
    print("\n✅ All done. Saved to mixesdb_danielbell_tracklists.csv")
