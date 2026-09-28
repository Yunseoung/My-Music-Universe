import re
import json
import os
from collections import Counter

def extract_music_fast(html_file, output_file):
    print(f"🚀 '{html_file}' 파일을 읽는 중... (메모리 로딩)")
    
    if not os.path.exists(html_file):
        print(f"❌ 오류: '{html_file}' 파일이 없습니다. 파일명을 확인해주세요.")
        return

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return

    print("🔍 데이터 검색 중... (HTML 파싱 건너뛰기)")

    # 정규표현식으로 <div class="content-cell">...</div> 블록을 직접 찾습니다.
    # 이 방식은 BS4보다 훨씬 빠릅니다.
    # HTML 구조: <div class="content-cell">...<a href="...">제목</a>...<a href="...">채널</a>...</div>
    
    # 1. 모든 content-cell 블록 찾기
    cell_pattern = re.compile(r'<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.*?)</div>', re.DOTALL)
    cells = cell_pattern.findall(content)
    
    # 만약 위 패턴으로 안 잡히면 조금 더 단순한 패턴 시도
    if not cells:
        cell_pattern = re.compile(r'<div class="content-cell[^"]*">(.*?)</div>', re.DOTALL)
        cells = cell_pattern.findall(content)

    print(f"   - 총 {len(cells)}개의 시청 기록 블록을 찾았습니다.")
    
    music_records = []
    
    # 2. 각 블록에서 정보 추출
    print("🎵 음악 데이터 필터링 중...")
    
    # 링크(a 태그) 추출용 패턴
    link_pattern = re.compile(r'<a href="([^"]*)">([^<]*)</a>')
    
    count = 0
    for cell_html in cells:
        count += 1
        if count % 5000 == 0:
            print(f"   ... {count}개 처리 중")

        # 음악 판별 로직
        is_music = False
        
        # 텍스트 검사
        if "YouTube Music" in cell_html:
            is_music = True
        
        links = link_pattern.findall(cell_html)
        # links는 [('url', 'text'), ('url', 'text'), ...] 형태의 튜플 리스트
        
        if not is_music:
            for url, text in links:
                if "music.youtube.com" in url:
                    is_music = True
                    break
        
        # 채널명에 Topic/주제 포함 여부
        if not is_music and len(links) >= 2:
            channel_name = links[1][1]
            if "Topic" in channel_name or "주제" in channel_name:
                is_music = True
        
        if is_music and len(links) >= 2:
            song_title = links[0][1]
            raw_artist = links[1][1]
            
            # 아티스트 이름 정리
            artist_name = raw_artist.replace(" - Topic", "").replace(" - 주제", "").strip()
            
            music_records.append({
                "artist": artist_name,
                "song": song_title
            })

    print(f"✅ 필터링 완료! 총 {len(music_records)}개의 음악 데이터를 확보했습니다.")

    if not music_records:
        print("⚠️ 음악 데이터를 찾지 못했습니다. HTML 파일 형식이 예상과 다를 수 있습니다.")
        return

    # ---------------------------------------------------------
    # 데이터 구조화 (이전과 동일)
    # ---------------------------------------------------------
    print("📦 시각화 데이터 패키징 중...")

    artist_counts = Counter(r['artist'] for r in music_records)
    top_artists = [art for art, cnt in artist_counts.most_common(50)]
    
    nodes = [{"id": "ME", "group": 0, "size": 100, "count": len(music_records)}]
    links = []

    for artist in top_artists:
        count = artist_counts[artist]
        nodes.append({
            "id": artist, 
            "group": 1, 
            "size": count,
            "count": count
        })
        links.append({"source": "ME", "target": artist})
        
        unique_songs = list(set([r['song'] for r in music_records if r['artist'] == artist]))[:15]
        
        for song in unique_songs:
            song_id = f"{artist}_{song}"
            nodes.append({
                "id": song_id,
                "name": song,
                "artist": artist,
                "group": 2,
                "size": 5
            })
            links.append({"source": artist, "target": song_id})

    final_data = {"nodes": nodes, "links": links}
    js_content = f"window.universeData = {json.dumps(final_data, ensure_ascii=False)};"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"🎉 성공! '{output_file}' 파일이 생성되었습니다.")

if __name__ == "__main__":
    extract_music_fast('시청 기록.html', 'universe_data.js')