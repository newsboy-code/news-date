import requests
from bs4 import BeautifulSoup
import json

def get_koreawho_profiles():
    # 정확히 찾아주신 jsp 목록 페이지 주소
    url = "https://www.koreawho.com/profile_list.jsp" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # JSP 목록 페이지는 보통 <table> 또는 <div> 안에 반복되는 구조를 가집니다.
        # 모든 a 태그를 뒤져서 프로필 상세 주소를 찾습니다.
        all_links = soup.find_all('a', href=True)

        for a in all_links:
            href = a['href']
            # 프로필 상세 페이지 패턴 (예: profile_view.jsp 등)을 찾습니다.
            if 'profile' in href or 'view' in href:
                title = a.get_text(strip=True)
                
                # 이름이 너무 짧으면 패스 (보통 인물명은 2자 이상)
                if len(title) < 2: continue
                
                # 주소 완성
                link = href if href.startswith('http') else "https://www.koreawho.com/" + href.lstrip('/')
                
                # 근처에 있는 이미지(증명사진 등) 찾기
                # 보통 a태그 안이나 바로 옆에 img 태그가 있습니다.
                img_tag = a.find('img') or (a.parent.find('img') if a.parent else None)
                thumb = ""
                if img_tag:
                    thumb = img_tag.get('src') or img_tag.get('data-src')
                    if thumb and not thumb.startswith('http'):
                        thumb = "https://www.koreawho.com/" + thumb.lstrip('/')

                # 중복 데이터 방지
                if not any(obj['link'] == link for obj in articles):
                    articles.append({
                        "title": title,
                        "link": link,
                        "thumbnail": thumb or "https://www.koreawho.com/favicon.ico"
                    })
            
            if len(articles) >= 20: break # 상위 20명만
                
        return articles
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

# 데이터 실행 및 출력
data = get_koreawho_profiles()
print(f"--- 결과 리포트 ---")
print(f"찾은 데이터 개수: {len(data)}")
if len(data) > 0:
    print(f"첫 번째 데이터 예시: {data[0]['title']}")
print(f"------------------")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
