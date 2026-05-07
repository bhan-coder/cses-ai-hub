import streamlit as st
import urllib.request
import urllib.parse
import json
import difflib

# 1. 페이지 설정 및 디자인 (CSS 주입)
st.set_page_config(page_title="CSES Insight Hub", page_icon="💡", layout="wide")

# 아까 보여주신 디자인과 비슷하게 만들기 위한 커스텀 스타일
st.markdown("""
    <style>
    /* 메인 배경 및 폰트 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F9FAFB; }
    
    /* 카드 디자인 */
    .news-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border: 1px solid #F3F4F6;
        transition: transform 0.2s;
    }
    .news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    /* 태그 디자인 */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .tag-ai { background-color: #FEE2E2; color: #EF4444; } /* AI 뉴스 태그 */
    .tag-edu { background-color: #ECFDF5; color: #10B981; } /* 교육 태그 */
    
    /* 제목 및 텍스트 스타일 */
    .card-title { font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 8px; text-decoration: none; }
    .card-desc { font-size: 15px; color: #4B5563; line-height: 1.6; }
    .card-link { color: #3B82F6; font-weight: 600; text-decoration: none; font-size: 14px; }
    
    /* 상단 헤더 섹션 */
    .header-box { background-color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; border: 1px solid #E5E7EB; }
    .header-title { font-size: 42px; font-weight: 800; color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# 2. 상단 헤더 섹션 (이미지와 비슷한 레이아웃)
with st.container():
    st.markdown("""
        <div class="header-box">
            <p style="color: #EF4444; font-weight: bold; margin-bottom: 10px;">CSES Insight Hub</p>
            <h1 class="header-title">연구원을 위한<br>AI 인사이트 스테이션</h1>
            <p style="color: #6B7280; font-size: 18px; margin-top: 20px;">네이버 뉴스 기반의 실시간 기술 동향과 맞춤형 교육 정보를 큐레이션합니다.</p>
        </div>
    """, unsafe_allow_html=True)

# 3. 탭 메뉴 구성
tab1, tab2 = st.tabs(["📰 AI 뉴스 센터", "🎓 교육 스테이션"])

# --- 탭 1: 뉴스 센터 ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("최신 기술 동향")
    with col2:
        btn = st.button("🔄 실시간 뉴스 업데이트", use_container_width=True)

    if btn:
        with st.spinner("언론사별 데이터를 수집 중..."):
            client_id = "_HfjBuozxC3_KxW5BErl"
            client_secret = "kjeNP9XVUe"
            keyword = "인공지능 AI 신기술"
            encText = urllib.parse.quote(keyword)
            target_media_domains = ["yna.co.kr", "donga.com", "joongang.co.kr", "chosun.com", "hankookilbo.com"]
            final_news_list = []

            for start_idx in range(1, 201, 100):
                url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&display=100&start={start_idx}&sort=sim"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                try:
                    response = urllib.request.urlopen(request)
                    result = json.loads(response.read().decode('utf-8'))
                    for item in result['items']:
                        title = item['title'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
                        link = item['originallink']
                        desc = item['description'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
                        if not any(domain in link for domain in target_media_domains): continue
                        if any(difflib.SequenceMatcher(None, title, news['title']).ratio() > 0.6 for news in final_news_list): continue
                        final_news_list.append({'title': title, 'desc': desc, 'link': link})
                        if len(final_news_list) >= 6: break
                except: pass
                if len(final_news_list) >= 6: break

            # 디자인된 카드 형태로 뉴스 출력
            if final_news_list:
                cols = st.columns(2) # 2열 격자로 배치
                for i, news in enumerate(final_news_list):
                    with cols[i % 2]:
                        st.markdown(f"""
                            <div class="news-card">
                                <span class="tag tag-ai">AI 뉴스</span>
                                <div class="card-title">{news['title']}</div>
                                <p class="card-desc">{news['desc'][:100]}...</p>
                                <a href="{news['link']}" target="_blank" class="card-link">기사 원문 보기 →</a>
                            </div>
                        """, unsafe_allow_html=True)

# --- 탭 2: 교육 스테이션 ---
with tab2:
    st.subheader("추천 교육 프로그램")
    
    # 교육 카드 렌더링
    edu_list = [
        {"provider": "KIRD", "title": "AI 리서치 자동화 기초", "tag": "무료", "desc": "생성형 AI를 활용한 효율적인 자료 수집 및 분석 노하우"},
        {"provider": "KSA", "title": "AI 경영시스템 표준화", "tag": "유료", "desc": "ISO 42001 기반의 AI 신뢰성 및 거버넌스 구축 전략"},
        {"provider": "통계교육원", "title": "R을 활용한 데이터 분석", "tag": "무료", "desc": "통계 에디팅 및 비정형 데이터 정제 실무 과정"}
    ]
