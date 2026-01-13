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
        
        # 모든 링크 탐색
        all_links = soup.find_all('a', href=True)

        for a in all_links:
            href = a['href']
            title = a.get_text(strip=True)
            
            # 1. 뉴스 기사 링크 (javascript 형태) 변환
            # 예: javascript:article_view('7561') -> https://www.koreawho.com/news/view.php?idx=7561
            js_match = re.search(r"article_view\('(\d+)'\)", href)
            if js_match:
                idx = js_match.group(1)
                link = f"https://www.koreawho.com/news/view.php?idx={idx}"
            
            # 2. 프로필 링크 변환
            elif '/profile/' in href:
                link = "https://www.koreawho.com" + href if href.startswith('/') else "https://www.koreawho.com/" + href
            
            else:
                continue # 그 외 잡다한 링크는 무시

            # 제목 정제 및 짧은 제목 제외
            title = title.replace('•', '').strip()
            if len(title) < 5 or title == "PROFILE": continue

            # 이미지 찾기
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

# 데이터 실행 및 저장
data = get_koreawho_data()
print(f"총 {len(data)}개의 유효한 링크를 생성했습니다.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
