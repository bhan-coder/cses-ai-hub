import streamlit as st
import urllib.request
import urllib.parse
import json
import difflib
import google.generativeai as genai

# 웹사이트 전체 화면 설정
st.set_page_config(page_title="CSES AI Insight Hub", page_icon="💡", layout="wide")

st.title("💡 CSES AI Insight Hub")
st.markdown("**연구원을 위한 스마트 리서치 파트너**")
st.divider()

# 화면을 두 개의 탭으로 나눕니다.
tab1, tab2 = st.tabs(["📰 일일 AI 뉴스 브리핑", "🎓 연구원 맞춤형 AI 교육"])

# ==========================================
# 첫 번째 탭: AI 뉴스 요약 (거창한 내용 제거!)
# ==========================================
with tab1:
    st.subheader("오늘의 핵심 AI 동향")
    st.markdown("최신 AI 뉴스를 수집하고 핵심만 빠르게 요약합니다.")
    
    if st.button("🔄 AI 뉴스 브리핑 생성하기", type="primary"):
        with st.spinner("뉴스를 수집하고 요약본을 작성 중입니다. 잠시만 기다려주세요..."):
            
            # 1. API 설정
            gemini_api_key = "AIzaSyCZJy6Lw9LZjfVc2sAqbv7elVSH8PFbwnU" 
            genai.configure(api_key=gemini_api_key)
            
            # 💡 에러 방지를 위해 가장 범용적인 모델 사용
            model = genai.GenerativeModel('gemini-1.5-flash') 

            client_id = "_HfjBuozxC3_KxW5BErl"  
            client_secret = "kjeNP9XVUe"        

            # 2. 네이버 뉴스 수집 로직
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
                        originallink = item['originallink']
                        
                        if not any(domain in originallink for domain in target_media_domains): continue
                        if any(difflib.SequenceMatcher(None, title, news['title']).ratio() > 0.6 for news in final_news_list): continue

                        final_news_list.append({
                            'title': title,
                            'desc': item['description'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
                        })
                        if len(final_news_list) >= 5: break 
                except Exception: pass
                if len(final_news_list) >= 5: break

            # 3. Gemini 요약 로직 (심플하게 변경!)
            news_text_for_ai = ""
            for idx, news in enumerate(final_news_list):
                news_text_for_ai += f"[{idx+1}번 기사] 제목: {news['title']} / 내용: {news['desc']}\n"

            prompt = f"""
            아래 5개의 최신 AI 뉴스를 읽고, 바쁜 연구원들이 아침에 빠르게 읽을 수 있도록 요약해줘.
            거창한 분석이나 사회적 가치 연결 같은 건 필요 없고, 딱 팩트 위주로 심플하게 적어줘.

            [작성 형식]
            1. 🌟 오늘의 AI 트렌드 한 줄 요약
            2. 📰 주요 기사 3줄 요약 (가장 중요한 기사 3개만 골라서 각각 1~2줄로 요약)

            [오늘의 뉴스]
            {news_text_for_ai}
            """

            try:
                response = model.generate_content(prompt)
                st.success("브리핑 생성이 완료되었습니다!")
                with st.container(border=True):
                    st.markdown(response.text)
            except Exception as e:
                # 에러 발생 시 대처법 안내 추가
                st.error(f"구글 AI 서버 응답 오류가 발생했습니다. (에러코드: {e})")
                st.info("💡 팁: 깃허브 app.py 코드에서 'gemini-1.5-flash'를 'gemini-1.0-pro'로 변경해 보세요!")

# ==========================================
# 두 번째 탭: AI 교육 및 학습 추천 (정적 콘텐츠)
# ==========================================
with tab2:
    st.subheader("주요 교육 기관별 추천 강의")
    st.markdown("연구원의 실무 역량 강화를 위한 외부 및 내부 AI 교육 리스트입니다.")
    
    # 표(Table) 형태로 교육 리스트 출력
    st.markdown("""
    | 주최 기관 | 강의명 | 교육 내용 | 비용 |
    | :--- | :--- | :--- | :--- |
    | **한국표준협회(KSA)** | AI 경영시스템(ISO 42001) | AI 신뢰성 및 표준화 전략 | 150,000원 |
    | **KIRD (알파캠퍼스)** | AI 리서치 자동화 기초 | 생성형 AI 활용 자료 수집 및 분석 | 무료 |
    | **통계교육원** | R을 활용한 데이터 에디팅 | 통계 데이터 정제 및 비정형 데이터 분석 | 무료 |
    | **마소캠퍼스** | AI 보고서 자동화 실무 | 딥리서치 및 학술 보고서 초안 작성 | 120,000원 |
    """)
    
    st.divider()
    
    st.subheader("나의 레벨에 맞는 강의 추천")
    # 화면을 3분할해서 카드 형태로 예쁘게 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🌱 **입문자 코스**\n\nAI 기초 개념 이해 및 프롬프트 엔지니어링 활용법 (ChatGPT, Gemini 등 기본 활용)")
        
    with col2:
        st.warning("⚙️ **중급자 코스**\n\n데이터 분석 도구 연동 및 R/Python 통계 자동화 실무")
        
    with col3:
        st.error("👑 **전문가 코스**\n\n독자적 AI 모델 미세 조정 및 머신러닝 알고리즘 설계")
