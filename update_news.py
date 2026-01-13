import requests
from bs4 import BeautifulSoup
import json

def get_koreawho_news():
    url = "https://www.koreawho.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # 'item' 클래스나 'h2' 태그를 포함한 링크 위주로 탐색
        items = soup.find_all(['div', 'li'], class_=['item', 'list-item', 'article'])
        
        # 만약 아이템 그룹을 못 찾으면 모든 a 태그에서 기사처럼 보이는 것 추출
        if not items:
            items = soup.find_all('a', href=True)

        for item in items:
            try:
                # a 태그 찾기
                a_tag = item if item.name == 'a' else item.find('a')
                if not a_tag or not a_tag.get('href'): continue
                
                link = a_tag['href']
                if 'view.php' not in link and '/news/' not in link: continue # 기사 링크 형태만 필터링
                
                if not link.startswith('http'):
                    link = "https://www.koreawho.com" + link
                
                title = a_tag.text.strip()
                if len(title) < 10: continue # 너무 짧은 텍스트 제외

                img_tag = item.find('img') if item.name != 'a' else item.find_previous('img')
                thumb = ""
                if img_tag:
                    thumb = img_tag.get('src') or img_tag.get('data-src')
                    if thumb and not thumb.startswith('http'):
                        thumb = "https://www.koreawho.com" + thumb

                if not any(obj['link'] == link for obj in articles):
                    articles.append({
                        "title": title,
                        "link": link,
                        "thumbnail": thumb or "https://www.koreawho.com/favicon.ico"
                    })
            except:
                continue
            if len(articles) >= 15: break
                
        return articles
    except Exception as e:
        print(f"Error: {e}")
        return []

# 실행 및 강제 출력
data = get_koreawho_news()
print(f"### RESULT_START ###")
print(f"추출된 기사 개수: {len(data)}")
print(f"### RESULT_END ###")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
