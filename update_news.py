import requests
from bs4 import BeautifulSoup
import json

def get_koreawho_news():
    url = "https://www.koreawho.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # 방법 1: 'item' 클래스 전체 탐색
        items = soup.find_all('div', class_='item')
        
        # 만약 위 방법으로 안 찾아지면 방법 2: 모든 리스트 아이템 탐색
        if not items:
            items = soup.select('ul.list-contents li') or soup.select('.list-item')

        for item in items[:15]:
            try:
                # 1. 제목과 링크 찾기
                a_tag = item.find('a')
                if not a_tag: continue
                
                link = a_tag.get('href', '')
                if not link.startswith('http'):
                    link = "https://www.koreawho.com" + link
                
                # 제목 텍스트 (h2, h3 또는 strong 태그 등 우선순위 확인)
                title_tag = item.find(['h2', 'h3', 'strong', 'p'])
                title = title_tag.text.strip() if title_tag else a_tag.text.strip()
                if not title: continue

                # 2. 썸네일 이미지 찾기
                img_tag = item.find('img')
                thumb = ""
                if img_tag:
                    # 다양한 이미지 소스 속성 대응
                    thumb = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('srcset', '').split(' ')[0]
                    if thumb and not thumb.startswith('http'):
                        thumb = "https://www.koreawho.com" + thumb
                
                # 기본 이미지 (썸네일이 없을 경우를 대비한 언론사 로고나 더미 이미지)
                if not thumb:
                    thumb = "https://www.koreawho.com/favicon.ico"

                articles.append({
                    "title": title,
                    "link": link,
                    "thumbnail": thumb
                })
            except Exception as e:
                print(f"항목 파싱 오류: {e}")
                continue
                
        return articles
    except Exception as e:
        print(f"사이트 접속 오류: {e}")
        return []

# 데이터 실행 및 저장
news_data = get_koreawho_news()
print(f"추출된 기사 개수: {len(news_data)}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
