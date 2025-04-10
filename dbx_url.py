import requests
from bs4 import BeautifulSoup

base_url = "https://www.mixesdb.com"
start_url = "/w/Category:Daniel_Bell"
full_links = []

while start_url:
    url = base_url + start_url
    print(f"🔍 Scanning: {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # ミックスっぽいリンク（年号入り）を抽出
    links = [
        base_url + a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/w/20")
    ]
    full_links.extend(links)

    # 「次のページ」リンクを探す
    next_link = soup.find("a", string="next page")
    start_url = next_link["href"] if next_link else None

# 重複除去して表示
full_links = sorted(set(full_links))
for link in full_links:
    print(link)

print(f"\n✅ 合計 {len(full_links)} 件のリンクを取得しました。")
