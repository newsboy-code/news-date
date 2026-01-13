import requests
from bs4 import BeautifulSoup
import json

def get_koreawho_news():
    # 1. 실제 크롬 브라우저인 것처럼 헤더 정보를 강화합니다.
    url = "https://www.koreawho.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    
    try:
        # 2. 세션을 사용하여 쿠키 등을 처리합니다.
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        print(f"응답 상태 코드: {response.status_code}") # 200이 나와야 정상
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # 3. KoreaWho 사이트의 소스를 직접 분석한 결과, 기사 아이템을 찾는 더 넓은 범위의 태그를 설정합니다.
        # 메인 페이지의 모든 링크를 뒤져서 기사 링크처럼 보이는 것을 찾습니다.
        all_links = soup.find_all('a', href=True)
        
        for a in all_links:
            link = a['href']
            # 기사 주소 특징이 보통 /news/view.php 또는 특정 패턴이 있다면 필터링 가능합니다.
            # 일단 모든 기사 리스트를 수집해봅니다.
            title = a.text.strip()
            
            # 제목이 너무 짧거나 없는 것은 제외
            if len(title) < 10: continue
            
            if not link.startswith('http'):
                link = "https://www.koreawho.com" + link
            
            # 중복 제거 및 이미지 찾기
            if not any(article['link'] == link for article in articles):
                img_tag = a.find_parent().find('img') if a.find_parent() else None
                thumb = ""
                if img_tag:
                    thumb = img_tag.get('src') or img_tag.get('data-src', '')
                    if thumb and not thumb.startswith('http'):
                        thumb = "https://www.koreawho.com" + thumb
                
                articles.append({
                    "title": title,
                    "link": link,
                    "thumbnail": thumb or "https://www.koreawho.com/favicon.ico"
                })
            
            if len(articles) >= 15: break # 15개까지만
                
        return articles
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

news_data = get_koreawho_news()
print(f"추출된 기사 개수: {len(news_data)}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
