import streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# [설정] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Archetype Explorer",
    page_icon="🗺️",
    layout="wide"
)

# ---------------------------------------------------------
# [스타일] CSS: 카드형 버튼, 진행바, 폰트 디자인
# ---------------------------------------------------------
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; color: #1E3A8A; }
    .scenario-text { font-size:18px; line-height:1.6; color: #333; background-color:#F3F4F6; padding:20px; border-radius:10px; margin-bottom:20px; }
    .stButton>button { 
        width: 100%; 
        height: 100px; 
        border-radius: 15px; 
        border: 2px solid #E5E7EB; 
        font-size: 18px; 
        transition: all 0.3s;
    }
    .stButton>button:hover { 
        border-color: #3B82F6; 
        background-color: #EFF6FF; 
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# [상태 관리] 세션 스테이트 초기화
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1  # 1:장소선택, 2:도구선택, 3:대화시작
if "archetype" not in st.session_state:
    st.session_state.archetype = {"loc": "", "tool": "", "loc_desc": "", "tool_desc": ""}
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# [연결] Gemini API 연결 (Secrets 사용)
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("🚨 보안 키 오류: Streamlit Secrets를 확인하세요.")
    st.stop()

genai.configure(api_key=API_KEY)

# 시스템 프롬프트 로드
try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    st.error("시스템 프롬프트가 없습니다.")
    st.stop()

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# ---------------------------------------------------------
# [UI 구성] 헤더 및 진행바
# ---------------------------------------------------------
st.title("🗺️ Self-Discovery to Product")
st.caption("당신의 경험을 세계관이 담긴 시나리오로 해석합니다.")

# 진행률 표시 (Step에 따라 33%, 66%, 100%)
progress_value = 33 if st.session_state.step == 1 else (66 if st.session_state.step == 2 else 100)
st.progress(progress_value, text=f"탐험 진행률: {progress_value}%")

st.divider()

# ---------------------------------------------------------
# [Phase 1] 정체성 탐색 - 고대 도시
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="big-font">Phase 1. 잊혀진 고대 도시</p>', unsafe_allow_html=True)
    st.markdown('<div class="scenario-text">당신은 안개에 싸인 잊혀진 고대 도시에 도착했습니다.<br>이곳에 머물 수 있는 시간은 단 3시간.<br>본능적으로 당신의 발길이 향하는 곳은 어디입니까?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 시장과 광장\n(사람, 교류, 흐름)"):
            st.session_state.archetype["loc"] = "시장"
            st.session_state.archetype["loc_desc"] = "연결과 소통"
            st.session_state.step = 2
            st.rerun()
        if st.button("📚 도서관과 기록실\n(원칙, 지식, 체계)"):
            st.session_state.archetype["loc"] = "도서관"
            st.session_state.archetype["loc_desc"] = "시스템과 철학"
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🏠 주거지와 부엌\n(생활, 돌봄, 디테일)"):
            st.session_state.archetype["loc"] = "주거지"
            st.session_state.archetype["loc_desc"] = "공감과 디테일"
            st.session_state.step = 2
            st.rerun()
        if st.button("🛠️ 공방과 대장간\n(기술, 해결, 창조)"):
            st.session_state.archetype["loc"] = "공방"
            st.session_state.archetype["loc_desc"] = "문제해결과 기술"
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# [Phase 2] 도구 발견 - 역량 파악
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.markdown('<p class="big-font">Phase 2. 낡은 가죽 가방</p>', unsafe_allow_html=True)
    loc_name = st.session_state.archetype['loc']
    st.markdown(f'<div class="scenario-text">당신은 <b>[{loc_name}]</b>에 도착했습니다.<br>그곳에서 낡은 가죽 가방을 발견하고 열어봅니다.<br>가장 먼저 손에 잡힌 도구는 무엇입니까?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 돋보기\n(분석, 검증, 발견)"):
            st.session_state.archetype["tool"] = "돋보기"
            st.session_state.archetype["tool_desc"] = "데이터와 분석"
            st.session_state.step = 3
            st.rerun()
        if st.button("🧭 나침반\n(방향, 기획, 전략)"):
            st.session_state.archetype["tool"] = "나침반"
            st.session_state.archetype["tool_desc"] = "전략과 기획"
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("✒️ 깃펜\n(기록, 설득, 스토리)"):
            st.session_state.archetype["tool"] = "깃펜"
            st.session_state.archetype["tool_desc"] = "브랜딩과 마케팅"
            st.session_state.step = 3
            st.rerun()
        if st.button("🔧 수리도구\n(개선, 운영, 최적화)"):
            st.session_state.archetype["tool"] = "수리도구"
            st.session_state.archetype["tool_desc"] = "최적화와 실행"
            st.session_state.step = 3
            st.rerun()

# ---------------------------------------------------------
# [Phase 3] 가치 증명 - AI 인터뷰
# ---------------------------------------------------------
elif st.session_state.step == 3:
    # 1. AI의 첫 질문 생성 (최초 1회만 실행)
    if not st.session_state.messages:
        loc = st.session_state.archetype['loc']
        tool = st.session_state.archetype['tool']
        
        # 사용자에게 보여줄 안내 문구
        intro_text = f"""
        📜 **탐험 보고서**
        - **방문 구역:** {loc} ({st.session_state.archetype['loc_desc']})
        - **획득 도구:** {tool} ({st.session_state.archetype['tool_desc']})
        
        가치 기록가가 당신의 선택을 분석하여 '원형(Archetype)'을 정의하고 있습니다...
        """
        st.info(intro_text)
        
        # AI에게 보낼 첫 프롬프트 (화면엔 안 보이고 백그라운드 전송)
        initial_prompt = f"나는 고대 도시에서 [{loc}]을(를) 선택했고, 가방에서 [{tool}]을(를) 꺼냈어. 나의 원형(Archetype)을 정의하고, 내 실제 경험을 묻는 첫 질문을 던져줘."
        
        try:
            with st.spinner("가치 기록가가 당신의 기록을 읽고 있습니다..."):
                chat = model.start_chat(history=[])
                response = chat.send_message(initial_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

    # 2. 채팅 인터페이스 표시
    st.markdown('<p class="big-font">Phase 3. 가치 증명</p>', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. 사용자 입력 처리
    if prompt := st.chat_input("당신의 경험을 들려주세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("✍️ *기록 중...*")
            
            try:
                # 대화 히스토리 구성
                history = []
                # 시스템 프롬프트는 model 생성 시 들어갔으므로, 여기선 대화 내역만
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=history[:-1]) # 마지막 유저 메시지 제외하고 히스토리 전달
                response = chat.send_message(prompt) # 마지막 메시지 전송
                
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
                # 결과(JSON) 감지 시 축하 이펙트
                if "{" in response.text and "}" in response.text and "신뢰도" in response.text:
                    st.balloons()
                    st.success("🎉 탐험이 완료되었습니다! 당신의 고유한 가치가 기록되었습니다.")
                    
            except Exception as e:
                message_placeholder.error(f"Error: {e}")