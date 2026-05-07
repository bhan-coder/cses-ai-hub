import streamlit as st
import urllib.request
import urllib.parse
import json
import difflib
import google.generativeai as genai

# 웹사이트 전체 화면 설정
st.set_page_config(page_title="CSES AI Insight Hub", page_icon="💡", layout="wide")

st.title("💡 CSES AI Insight Hub")
st.markdown("**AI로 그리는 사회적 가치의 미래, 연구원을 위한 스마트 리서치 파트너**")
st.divider()

# 버튼을 누르면 크롤링과 요약을 시작합니다.
if st.button("🔄 오늘의 AI 인사이트 리포트 생성하기", type="primary"):
    
    with st.spinner("네이버 뉴스 수집 및 Gemini AI가 리포트를 작성 중입니다. 잠시만 기다려주세요..."):
        # 1. API 설정
        gemini_api_key = "AIzaSyCZJy6Lw9LZjfVc2sAqbv7elVSH8PFbwnU" # 연구원님 키
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro') # 안정적인 모델로 설정

        client_id = "_HfjBuozxC3_KxW5BErl"  
        client_secret = "kjeNP9XVUe"        

        # 2. 뉴스 수집 로직
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

        # 3. Gemini 요약 로직
        news_text_for_ai = ""
        for idx, news in enumerate(final_news_list):
            news_text_for_ai += f"[{idx+1}번 기사] 제목: {news['title']} / 내용: {news['desc']}\n"

        prompt = f"""
        너는 CSES(사회적가치연구원)의 수석 AI 연구원이야. 
        아래 5개의 최신 AI 뉴스를 읽고, '오늘의 AI 인사이트 리포트'를 작성해줘.

        [작성 형식]
        1. 🌟 오늘의 AI 트렌드 한 줄 요약: (핵심만)
        2. 📰 주요 기사 3줄 요약: (중요 기사 3개)
        3. 💡 연구원 적용 포인트: (사회적 가치 측정과 연결)

        [오늘의 뉴스]
        {news_text_for_ai}
        """

        try:
            response = model.generate_content(prompt)
            # 4. 웹사이트 화면에 예쁘게 출력하기
            st.success("리포트 생성이 완료되었습니다!")
            
            # 박스 안에 결과물 띄우기
            with st.container(border=True):
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"AI 요약 중 오류가 발생했습니다: {e}")
