---

### **2. `app.py` (직관적이고 차가운 UI/UX)**

불필요한 별자리, 장소 선택(Phase 1, 2)을 모두 날려버리고, **접속하자마자 비즈니스 피칭을 시작**하도록 UI를 전면 개편했습니다. 

기존 코드를 모두 지우고 아래 내용으로 덮어씌우십시오.

```python
import streamlit as st
import google.generativeai as genai
import time
import json

# ---------------------------------------------------------
# [설정] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Direct Value Monetizer",
    page_icon="💼",
    layout="centered"
)

# ---------------------------------------------------------
# [스타일] CSS: 냉철한 비즈니스 톤 (Dark Navy & White)
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0A192F;
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    p, li, span, div, h1, h2, h3 { color: #FFFFFF !important; }
    
    h1 {
        border-bottom: 2px solid #FFFFFF;
        padding-bottom: 10px;
        margin-bottom: 30px;
        font-weight: 700;
        letter-spacing: -1px;
    }

    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .report-card {
        background-color: #112240;
        border-left: 5px solid #64FFDA;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 10px 30px -15px rgba(2,12,27,0.7);
    }
    
    .report-card h3 { color: #64FFDA !important; font-size: 1.2rem; margin-top: 15px; margin-bottom: 5px; }
    .report-card p { font-size: 1.1rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# [상태 관리]
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

# ---------------------------------------------------------
# [연결] Gemini API
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.warning("⚠️ API 키가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=API_KEY)

try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    st.error("🚨 system_prompt.md 파일이 없습니다.")
    st.stop()

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# ---------------------------------------------------------
# [UI 구성] 헤더
# ---------------------------------------------------------
st.title("💼 Direct Value Monetizer")
st.markdown("당신의 경험을 즉시 판매 가능한 상품(Product)으로 전환합니다.")

# ---------------------------------------------------------
# [대화 로직]
# ---------------------------------------------------------
if not st.session_state.messages:
    initial_prompt = "현재 하고 있는 일에 만족하십니까? 아니라면, 그 불만을 '돈이 되는 서비스'로 바꿀 때 당신은 누구에게 무엇을 팔 수 있습니까? 단도직입적으로 묻고 대화를 시작해."
    
    with st.spinner("Initializing Business Accelerator..."):
        chat = model.start_chat(history=[])
        response = chat.send_message(initial_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👔" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

if not st.session_state.is_finished:
    if prompt := st.chat_input("당신의 비즈니스 가설을 입력하십시오."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        st.session_state.turn_count += 1
        
        with st.chat_message("assistant", avatar="👔"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Analyzing market value...")
            
            history = [{"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]} for msg in st.session_state.messages]
            
            # 4턴 이상 진행 시 제안서 도출 유도
            final_instruction = ""
            if st.session_state.turn_count >= 4:
                final_instruction = "\n\n(SYSTEM: 대화가 충분히 진행되었습니다. 지금까지의 내용을 바탕으로 JSON 형태의 [비즈니스 가치 제안서]를 즉시 출력하십시오.)"
            
            try:
                chat = model.start_chat(history=history[:-1])
                response = chat.send_message(prompt + final_instruction)
                
                if "{" in response.text and "}" in response.text and "수익화전략" in response.text:
                    text_part = response.text.split("{")[0]
                    if text_part.strip():
                        message_placeholder.markdown(text_part)
                    
                    json_str = "{" + response.text.split("{", 1)[1] 
                    json_str = json_str.rsplit("}", 1)[0] + "}"
                    report_data = json.loads(json_str)
                    
                    # [비즈니스 가치 제안서 렌더링]
                    st.markdown(f"""
                    <div class='report-card'>
                        <h2>📄 비즈니스 가치 제안서 (Value Proposition)</h2>
                        <h3>▪ 핵심 서비스 (Core Service)</h3>
                        <p>{report_data.get('핵심서비스', '')}</p>
                        <h3>▪ 타겟 고객 (Target Audience)</h3>
                        <p>{report_data.get('타겟고객', '')}</p>
                        <h3>▪ 신뢰 근거 (Credibility Basis)</h3>
                        <p>{report_data.get('신뢰근거', '')}</p>
                        <h3>▪ 수익화 전략 (Monetization Strategy)</h3>
                        <p>{report_data.get('수익화전략', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.is_finished = True
                    st.rerun()
                else:
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
            except Exception as e:
                message_placeholder.error(f"Error: {e}")