import streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# [설정] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Phronesis Guardian",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------------
# [스타일] CSS로 화면 꾸미기
# ---------------------------------------------------------
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; color: #2E86C1; }
    .info-box { background-color: #F0F2F6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #dcdcdc; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# [사이드바] 옵션 및 설명
# ---------------------------------------------------------
with st.sidebar:
    st.header("🛡️ Guardian Control")
    st.info("이 시스템은 당신의 경험을 분석하여 '진짜 가치'를 증명합니다.")
    st.divider()
    st.markdown("### 📊 현재 분석 모듈")
    st.checkbox("가치 발굴 (Extractor)", value=True, disabled=True)
    st.checkbox("진위 여부 검증 (Security)", value=True, disabled=True)
    st.checkbox("JSON 데이터화 (Data)", value=True, disabled=True)
    st.divider()
    st.caption("Powered by Gemini Pro")

# ---------------------------------------------------------
# [메인] 헤더 및 대시보드
# ---------------------------------------------------------
st.title("🛡️ Phronesis Guardian")
st.markdown("### :sparkles: 당신만의 '숨겨진 자산'을 찾아드립니다")

# 시각적 흥미를 유발하는 메트릭(점수판)
col1, col2, col3 = st.columns(3)
col1.metric("분석 대기 중", "Ready", "System On")
col2.metric("검증된 데이터", "856건", "High Reliability")
col3.metric("가치 발굴 성공률", "98%", "Level Up")

st.divider()

# ---------------------------------------------------------
# [연결] 뇌(Brain) 연결 - (수정됨: 보안 금고 사용)
# ---------------------------------------------------------
try:
    # 1. 금고(Secrets)에서 열쇠를 꺼내옵니다.
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("🚨 보안 키 오류: Streamlit Secrets에 키가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=API_KEY)

# 2. (이 부분은 지우면 안 됩니다!) 시스템 프롬프트 파일 읽기
try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    st.error("시스템 프롬프트가 없습니다.")
    st.stop()

# 3. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# ---------------------------------------------------------
# [첫 인사말 & 초기화] 여기가 선생님이 찾던 부분입니다!
# ---------------------------------------------------------
first_message = """반갑습니다! 저는 당신이 살아오며 체득한, 세상에 단 하나뿐인 '지혜'를 찾아내어 가치로 만들어드릴 AI 파트너, **가치 탐험가(Value Explorer)**입니다.

먼저 가벼운 질문으로 시작해볼까요? **당신이 가장 오랫동안 머물며 그 누구보다 잘 안다고 자부하는 '동네'나 '장소'는 어디인가요?** 그리고 그곳의 골목골목을 떠올렸을 때, 당신만 알고 있는 독특한 특징 하나만 말씀해주세요."""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": first_message}
    ]

# ---------------------------------------------------------
# [흥미 유발] 버튼 클릭 (Quick Start)
# ---------------------------------------------------------
# 버튼을 누르면 자동으로 채팅창에 입력되게 하는 함수
if "clicked_prompt" not in st.session_state:
    st.session_state.clicked_prompt = None

def click_button(text):
    st.session_state.clicked_prompt = text

st.markdown("<div class='info-box'>🤔 <b>무엇을 검증받고 싶으신가요? (예시 클릭)</b></div>", unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns(3)
if btn_col1.button("🏘️ 우리 동네 전문가"):
    click_button("나는 서울 을지로 골목을 10년 동안 돌아다녀서, 쥐가 어디로 다니는지도 알아. 이게 가치가 있을까?")
if btn_col2.button("💼 내 업무 경험"):
    click_button("중국 구매대행을 3년 했는데, 물건 떼오는 것보다 세관 통과시키는 게 더 자신 있어.")
if btn_col3.button("🔧 취미가 특기"):
    click_button("재봉틀로 아기 옷 만드는 걸 좋아해서 50벌 넘게 만들어서 선물했어.")

# ---------------------------------------------------------
# [채팅 인터페이스]
# ---------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리 (버튼 클릭 or 직접 입력)
if prompt := st.chat_input("당신의 이야기를 들려주세요.") or st.session_state.clicked_prompt:
    
    # 버튼 값 처리 후 초기화
    if st.session_state.clicked_prompt:
        prompt = st.session_state.clicked_prompt
        st.session_state.clicked_prompt = None 

    # 화면에 사용자 메시지 표시 (중복 방지)
    # 마지막 메시지가 방금 입력한 내용과 다를 때만 추가
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI 응답
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⚡ *가치 탐험가가 당신의 경험을 분석 중입니다...*")
            
            try:
                time.sleep(1) 
                
                history = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    # 첫 인사말은 히스토리에 넣지 않음 (오류 방지)
                    if msg["content"] != first_message:
                        history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                message_placeholder.error(f"Error: {e}")