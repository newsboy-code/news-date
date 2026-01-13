import requests
from bs4 import BeautifulSoup
import json
import os

def get_koreawho_news():
    url = "https://www.koreawho.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    # KoreaWho 사이트 구조에 맞게 수정이 필요할 수 있습니다.
    # 일반적인 뉴스 사이트 태그 예시입니다.
    for item in soup.select('div.item')[:10]: # 최신 기사 10개
        try:
            title = item.select_one('h2').text.strip()
            link = item.select_one('a')['href']
            if not link.startswith('http'):
                link = "https://www.koreawho.com" + link
            thumb = item.select_one('img')['src']
            articles.append({"title": title, "link": link, "thumbnail": thumb})
        except:
            continue
    return articles

news_data = get_koreawho_news()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
