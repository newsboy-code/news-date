import requests
from bs4 import BeautifulSoup
import json
import re

def get_koreawho_data():
    url = "https://www.koreawho.com/profile_list.jsp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        all_links = soup.find_all('a', href=True)

        for a in all_links:
            href = a['href']
            title = a.get_text(" ", strip=True) # 태그 간 공백 추가하여 이름 붙음 방지
            
            # 1. 뉴스 기사 링크 처리 (javascript)
            js_match = re.search(r"article_view\('(\d+)'\)", href)
            if js_match:
                idx = js_match.group(1)
                link = f"https://www.koreawho.com/news/view.php?idx={idx}"
            
            # 2. 프로필 링크 처리 (중첩 방지 로직 추가)
            elif '/profile/' in href:
                # 이미 http가 포함되어 있다면 그대로 사용, 아니면 붙여주기
                if href.startswith('http'):
                    link = href
                else:
                    link = "https://www.koreawho.com/" + href.lstrip('/')
            
            else:
                continue

            # 불필요한 단어 및 짧은 제목 정제
            title = title.replace('•', '').strip()
            if len(title) < 5 or title.upper() == "PROFILE": continue

            # 이미지 추출
            img_tag = a.find('img') or (a.parent.find('img') if a.parent else None)
            thumb = ""
            if img_tag:
                thumb = img_tag.get('src') or img_tag.get('data-src')
                if thumb and not thumb.startswith('http'):
                    thumb = "https://www.koreawho.com/" + thumb.lstrip('/')

            if not any(obj['link'] == link for obj in articles):
                articles.append({
                    "title": title,
                    "link": link,
                    "thumbnail": thumb or "https://www.koreawho.com/favicon.ico"
                })
            
            if len(articles) >= 20: break
                
        return articles
    except Exception as e:
        print(f"Error: {e}")
        return []

data = get_koreawho_data()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
