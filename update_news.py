import requests
from bs4 import BeautifulSoup
import json

def get_koreawho_news():
    url = "https://www.koreawho.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # KoreaWho 사이트의 기사 리스트 구조 (실제 HTML 기반 수정)
        # 메인 페이지의 최신 기사 영역인 'item' 클래스를 타겟팅합니다.
        items = soup.select('div.item')
        
        for item in items[:12]: # 최근 12개 기사
            try:
                # 제목 추출
                title_tag = item.select_one('h2.title a') or item.select_one('h2 a')
                title = title_tag.text.strip()
                
                # 링크 추출
                link = title_tag['href']
                if not link.startswith('http'):
                    link = "https://www.koreawho.com" + link
                
                # 썸네일 이미지 추출
                img_tag = item.select_one('img')
                thumb = ""
                if img_tag:
                    # lazy loading 대응 (data-src 또는 src 확인)
                    thumb = img_tag.get('data-src') or img_tag.get('src', '')
                    if thumb and not thumb.startswith('http'):
                        thumb = "https://www.koreawho.com" + thumb
                
                articles.append({
                    "title": title,
                    "link": link,
                    "thumbnail": thumb
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue
                
        return articles
    except Exception as e:
        print(f"Error fetching site: {e}")
        return []

# 데이터 가져오기
news_data = get_koreawho_news()

# 결과가 비어있는지 확인용 출력
print(f"Found {len(news_data)} articles.")

# 파일 저장
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
