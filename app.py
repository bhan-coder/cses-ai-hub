<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSES AI Insight Hub | 맞춤형 교육 추천</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        .bg-cses-pink { background-color: #E6005A; }
        .text-cses-pink { color: #E6005A; }
        .border-cses-pink { border-color: #E6005A; }
        .bg-warm-base { background-color: #FAF9F7; }
        .hover-lift:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(230, 0, 90, 0.1); }
    </style>
</head>
<body class="bg-warm-base text-gray-900">

    <header class="fixed w-full z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <span class="text-xl font-black text-cses-pink">CSES INSIGHT</span>
            </div>
            <nav class="hidden md:flex gap-10 text-sm font-bold text-gray-600">
                <a href="#" class="hover:text-cses-pink">홈</a>
                <a href="#diagnosis" class="text-cses-pink">AI 교육 진단</a>
                <a href="#" class="hover:text-cses-pink">AI 뉴스</a>
            </nav>
        </div>
    </header>

    <section class="pt-32 pb-12 px-6">
        <div class="max-w-7xl mx-auto text-center">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">나에게 꼭 맞는 <span class="text-cses-pink">AI 성장 경로</span>를 찾아보세요</h1>
            <p class="text-gray-500">K-MOOC, KPC, KSA의 검증된 교육 과정을 추천해 드립니다.</p>
        </div>
    </section>

    <section id="diagnosis" class="py-12 px-6">
        <div class="max-w-4xl mx-auto">
            <div id="diagnosisCard" class="bg-white p-8 md:p-12 rounded-[40px] shadow-xl shadow-pink-100/50 border border-pink-50">
                
                <div id="step1">
                    <span class="text-cses-pink font-bold text-sm tracking-widest">STEP 01</span>
                    <h3 class="text-2xl font-bold mt-2 mb-8">관심 있는 연구 분야를 선택해주세요.</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <button onclick="nextStep('데이터 리터러시')" class="p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition group flex justify-between items-center">
                            <span class="font-bold text-lg">데이터 리터러시</span>
                            <span class="text-cses-pink opacity-0 group-hover:opacity-100">→</span>
                        </button>
                        <button onclick="nextStep('생성형 AI')" class="p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition group flex justify-between items-center">
                            <span class="font-bold text-lg">생성형 AI 모델링</span>
                            <span class="text-cses-pink opacity-0 group-hover:opacity-100">→</span>
                        </button>
                        <button onclick="nextStep('AI 거버넌스')" class="p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition group flex justify-between items-center">
                            <span class="font-bold text-lg">AI 윤리 및 거버넌스</span>
                            <span class="text-cses-pink opacity-0 group-hover:opacity-100">→</span>
                        </button>
                        <button onclick="nextStep('비즈니스 전략')" class="p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition group flex justify-between items-center">
                            <span class="font-bold text-lg">AI 비즈니스 전략</span>
                            <span class="text-cses-pink opacity-0 group-hover:opacity-100">→</span>
                        </button>
                    </div>
                </div>

                <div id="step2" class="hidden">
                    <span class="text-cses-pink font-bold text-sm tracking-widest">STEP 02</span>
                    <h3 class="text-2xl font-bold mt-2 mb-8">현재 본인의 역량 수준은 어떤가요?</h3>
                    <div class="space-y-4">
                        <button onclick="showResult('입문')" class="w-full p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition">
                            <p class="font-bold text-lg">Beginner (입문/기초)</p>
                            <p class="text-sm text-gray-500 mt-1">기본 개념을 익히고 활용 사례를 배우고 싶습니다.</p>
                        </button>
                        <button onclick="showResult('심화')" class="w-full p-6 border rounded-2xl text-left hover:border-cses-pink hover:bg-pink-50 transition">
                            <p class="font-bold text-lg">Advanced (중급/심화)</p>
                            <p class="text-sm text-gray-500 mt-1">실무 모델링이나 전문 표준/인증 과정을 희망합니다.</p>
                        </button>
                    </div>
                </div>

                <div id="result" class="hidden">
                    <div class="text-center mb-10">
                        <div class="inline-block p-4 bg-pink-50 rounded-full text-cses-pink mb-4">
                            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        </div>
                        <h3 class="text-3xl font-bold mb-2">맞춤 교육 추천 리스트</h3>
                        <p id="resultIntro" class="text-gray-600"></p>
                    </div>

                    <div id="courseContainer" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        </div>

                    <div class="text-center mt-12">
                        <button onclick="resetDiagnosis()" class="text-sm font-bold text-gray-400 hover:text-cses-pink underline underline-offset-4">다시 진단하기</button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script>
        let selectedField = '';
        
        // 교육 데이터베이스
        const courseData = {
            '데이터 리터러시': {
                '입문': [
                    { platform: 'KPC', title: '빅데이터 분석 및 시각화 실무', link: 'https://www.kpc.or.kr/edu/CourseDetail.do?pCourseId=65588', desc: '데이터 수집부터 시각화까지 핵심 기초 습득' },
                    { platform: 'K-MOOC', title: '인공지능의 기초 및 활용', link: 'https://www.kmooc.kr/view/course/detail/11696', desc: '비전공자도 이해하는 AI와 데이터의 기본 원리' }
                ],
                '심화': [
                    { platform: 'KPC', title: '파이썬 활용 빅데이터 분석 실무', link: 'https://www.kpc.or.kr/edu/CourseDetail.do?pCourseId=65604', desc: '파이썬을 이용한 전문적인 데이터 통계 분석' }
                ]
            },
            '생성형 AI': {
                '입문': [
                    { platform: 'KPC', title: '생성형 AI 활용 업무 혁신', link: 'https://www.kpc.or.kr/edu/CourseDetail.do?pCourseId=66324', desc: 'ChatGPT 등 생성형 AI를 실무에 즉시 적용하기' }
                ],
                '심화': [
                    { platform: 'K-MOOC', title: '딥러닝을 이용한 자연어 처리', link: 'https://www.kmooc.kr/view/course/detail/10542', desc: 'Transformer 및 최신 언어 모델 연구 구현' },
                    { platform: 'K-MOOC', title: '실무자를 위한 딥러닝 응용', link: 'https://www.kmooc.kr/view/course/detail/12100', desc: '복잡한 딥러닝 모델의 최적화 및 배포 방법' }
                ]
            },
            'AI 거버넌스': {
                '입문': [
                    { platform: 'KSA', title: 'AI 신뢰성 및 윤리 가이드라인', link: 'https://www.ksaedu.or.kr/course/course_list.html?cate=001', desc: '안전한 AI 도입을 위한 기본 규범 및 윤리 이해' }
                ],
                '심화': [
                    { platform: 'KSA', title: 'ISO/IEC 42001 (AI 경영시스템) 실무', link: 'https://www.ksaedu.or.kr/course/course_view.html?id=2534', desc: '국제 표준에 기반한 AI 경영 시스템 구축 및 인증' }
                ]
            },
            '비즈니스 전략': {
                '입문': [
                    { platform: 'KPC', title: 'AI 비즈니스 모델 수립 실무', link: 'https://www.kpc.or.kr/edu/CourseDetail.do?pCourseId=65604', desc: 'AI 기술을 사업화 전략으로 연결하는 방법' }
                ],
                '심화': [
                    { platform: 'KSA', title: 'AI 산업 표준화 동향 및 전략', link: 'https://www.ksaedu.or.kr/main.html', desc: '글로벌 표준 전쟁 속에서 우위를 점하는 기술 전략' }
                ]
            }
        };

        function nextStep(field) {
            selectedField = field;
            document.getElementById('step1').classList.add('hidden');
            document.getElementById('step2').classList.remove('hidden');
        }

        function showResult(level) {
            document.getElementById('step2').classList.add('hidden');
            document.getElementById('result').classList.remove('hidden');
            
            const intro = document.getElementById('resultIntro');
            intro.innerHTML = `<strong>${selectedField}</strong> 분야의 <strong>${level}</strong> 전문가를 목표로 하는<br>연구원님께 다음 교육 과정을 추천합니다.`;

            const container = document.getElementById('courseContainer');
            container.innerHTML = '';

            const recommendations = courseData[selectedField][level];
            
            recommendations.forEach(course => {
                const card = `
                    <div class="hover-lift bg-warm-base p-6 rounded-3xl border border-gray-100 flex flex-col h-full">
                        <div class="flex justify-between items-start mb-4">
                            <span class="text-[10px] font-bold px-3 py-1 rounded-full border border-cses-pink text-cses-pink bg-white uppercase tracking-tighter">${course.platform}</span>
                            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-tighter">${level}</span>
                        </div>
                        <h4 class="text-xl font-bold mb-3 leading-tight">${course.title}</h4>
                        <p class="text-sm text-gray-500 mb-8 flex-grow leading-relaxed">${course.desc}</p>
                        <a href="${course.link}" target="_blank" class="w-full bg-cses-pink text-white py-4 rounded-2xl font-bold text-center hover:opacity-90 transition shadow-lg shadow-pink-200">강의 바로가기</a>
                    </div>
                `;
                container.innerHTML += card;
            });
        }

        function resetDiagnosis() {
            document.getElementById('result').classList.add('hidden');
            document.getElementById('step1').classList.remove('hidden');
        }
    </script>
</body>
</html>
