import streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# [설정] 시스템 UI 구성 (여기가 간판입니다)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Phronesis Guardian System",
    page_icon="🛡️",
    layout="wide"  # 화면을 넓게 써서 대시보드 느낌 나게 변경
)

# 헤더 디자인
st.title("🛡️ Phronesis Guardian: 프리 에이전트 중재 시스템")
st.markdown("""
**System Status:** ✅ Online | **Role:** Mediator & Value Extractor
- **Module 1:** 가치 발굴 (Extractor)
- **Module 2:** 보안 및 매칭 (Security)
- **Module 3:** 소통 중재 (Mediator)
- **Module 4:** 보상 평가 (Reward)
""")
st.divider() # 구분선 추가

# ---------------------------------------------------------
# [연결] 뇌(Brain) 연결
# ---------------------------------------------------------
API_KEY = "AIzaSyDlTX-JaNtI4W8GngNHSl2VkT6G7GUG0x0"
genai.configure(api_key=API_KEY)

try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    st.error("❌CRITICAL ERROR: 시스템 프롬프트(system_prompt.md)가 로드되지 않았습니다.")
    st.stop()

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# ---------------------------------------------------------
# [인터페이스] 대화창 구현
# ---------------------------------------------------------
if "messages" not in st.session_state:
    # 시스템이 먼저 말을 걸도록 초기 메시지 설정
    st.session_state.messages = [
        {"role": "assistant", "content": "시스템이 가동되었습니다. 당신의 경력이나 프로젝트 경험을 입력해주시면, '가치 발굴 모듈'이 작동합니다."}
    ]

# 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력창 (문구 변경됨)
if prompt := st.chat_input("경험, 자격증, 혹은 프로젝트 이력을 입력하여 검증을 시작하십시오."):
    
    # 사용자 메시지 표시
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 응답 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔄 *Analyzing context... (가치 및 진위 여부 분석 중)*")
        
        try:
            # 약간의 딜레이를 줘서 진짜 분석하는 느낌 연출
            time.sleep(0.7) 
            
            history = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg["content"] != prompt:
                    # 시스템 첫 인사는 히스토리에 넣지 않음 (오류 방지)
                    if msg["content"] != "시스템이 가동되었습니다. 당신의 경력이나 프로젝트 경험을 입력해주시면, '가치 발굴 모듈'이 작동합니다.":
                         history.append({"role": role, "parts": [msg["content"]]})
            
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            message_placeholder.error(f"⚠️ System Error: {e}")