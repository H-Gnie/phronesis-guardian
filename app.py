import streamlit as st
import google.generativeai as genai
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ---------------------------------------------------------
# [설정] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Celestial Navigator",
    page_icon="🌌",
    layout="wide"
)

# ---------------------------------------------------------
# [함수] 구글 시트 저장 함수 (문자열 파싱 방식)
# ---------------------------------------------------------
def save_to_google_sheet(archetype, report_data, chat_history):
    try:
        # Secrets에서 JSON 문자열 가져와서 파싱하기
        json_str = st.secrets["GOOGLE_CREDENTIALS"]
        creds_dict = json.loads(json_str)
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # 시트 열기 (이름 정확해야 함!)
        sheet = client.open("Celestial_Logs").sheet1 

        # 데이터 준비
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conversation_log = ""
        for msg in chat_history:
            role = "👤 USER" if msg['role'] == "user" else "🤖 AI"
            conversation_log += f"[{role}] {msg['content']}\n\n"
        
        row_data = [
            timestamp,
            archetype['loc'],
            archetype['tool'],
            report_data.get('별자리명', ''),
            report_data.get('핵심가치', ''),
            report_data.get('한줄평', ''),
            conversation_log
        ]

        # 행 추가
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"🚨 데이터 저장 오류: {e}")
        return False

# ---------------------------------------------------------
# [스타일] CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #05080f 0%, #000000 100%);
        color: #FFFFFF !important;
        font-size: 1.15rem;
        line-height: 1.6;
    }
    p, li, span, div { color: #FFFFFF !important; }
    h1, h2, h3 {
        color: #FFD700 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    .scenario-box {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(0, 210, 255, 0.5);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        font-size: 1.25rem;
        text-align: center;
        color: #FFFFFF !important;
    }
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        height: 110px;
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(50, 50, 50, 0.9) 100%);
        color: #FFD700 !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: rgba(255, 215, 0, 0.15);
        border-color: #FFD700;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
        transform: scale(1.02);
    }
    .report-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# [상태 관리]
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1 
if "archetype" not in st.session_state:
    st.session_state.archetype = {"loc": "", "tool": "", "loc_desc": "", "tool_desc": ""}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0

# ---------------------------------------------------------
# [연결] Gemini API
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.warning("⚠️ Dev Mode: Secrets를 찾을 수 없습니다.")
    API_KEY = "YOUR_KEY_HERE"

genai.configure(api_key=API_KEY)

try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    st.error("🚨 시스템 프롬프트가 없습니다.")
    st.stop()

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

# ---------------------------------------------------------
# [UI 구성] 헤더
# ---------------------------------------------------------
st.title("🌌 Celestial Navigator")
st.markdown("### :sparkles: 당신의 무의식이 선택한 별자리")

if st.session_state.step < 3:
    progress_value = 33 if st.session_state.step == 1 else 66
else:
    progress_value = min(66 + (st.session_state.turn_count * 6), 100)

st.progress(progress_value, text=f"항해 진행률: {progress_value}%")
st.divider()

# ---------------------------------------------------------
# [Phase 1] 정체성 탐색
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown("""
    <div class='scenario-box'>
        "눈을 감고 상상해 보세요.<br>
        당신은 지금 낯선 행성의 한가운데 서 있습니다.<br>
        어디선가 바람이 불어오고, <strong>가장 먼저 당신의 감각을 자극하는 것</strong>은 무엇입니까?"
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗣️ 시끌벅적한 사람들의\n외침과 열기"):
            st.session_state.archetype["loc"] = "시장"
            st.session_state.step = 2
            st.rerun()
        if st.button("📖 오래된 종이 냄새와\n무거운 정적"):
            st.session_state.archetype["loc"] = "도서관"
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🍲 갓 구운 빵 냄새와\n따스한 온기"):
            st.session_state.archetype["loc"] = "주거지"
            st.session_state.step = 2
            st.rerun()
        if st.button("🔨 날카로운 금속 소리와\n뜨거운 불꽃"):
            st.session_state.archetype["loc"] = "공방"
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# [Phase 2] 도구 발견
# ---------------------------------------------------------
elif st.session_state.step == 2:
    loc = st.session_state.archetype['loc']
    st.markdown(f"""
    <div class='scenario-box'>
        "무의식이 이끄는 곳에 도착했습니다.<br>
        가방을 열어 <strong>손끝에 닿는 촉감만으로</strong> 하나의 도구를 꺼냅니다."
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 차갑고 매끄러운\n유리 렌즈"):
            st.session_state.archetype["tool"] = "돋보기"
            st.session_state.step = 3
            st.rerun()
        if st.button("🧭 끊임없이 흔들리는\n가느다란 바늘"):
            st.session_state.archetype["tool"] = "나침반"
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("✒️ 끝이 뾰족하고 가벼운\n새의 깃털"):
            st.session_state.archetype["tool"] = "깃펜"
            st.session_state.step = 3
            st.rerun()
        if st.button("🔧 묵직하고 기름때 묻은\n쇠막대"):
            st.session_state.archetype["tool"] = "수리도구"
            st.session_state.step = 3
            st.rerun()

# ---------------------------------------------------------
# [Phase 3] 가치 증명 & 엔딩 로직
# ---------------------------------------------------------
elif st.session_state.step == 3:
    if not st.session_state.messages:
        loc = st.session_state.archetype['loc']
        tool = st.session_state.archetype['tool']
        
        intro_text = f"""
        🕯️ **내면으로의 초대**
        
        당신은 **[{loc}]**에서 **[{tool}]**을 선택했습니다.
        이 선택 뒤에 숨겨진 당신의 진짜 마음을 들여다보겠습니다.
        """
        st.info(intro_text, icon="🕯️")
        
        initial_prompt = f"사용자는 [{loc}]과 [{tool}]을 선택했어. [대화의 대원칙]에 따라 그 순간의 '감정'을 묻는 첫 질문을 던져줘."
        
        try:
            with st.spinner("별자리 안내자가 당신의 마음을 읽고 있습니다..."):
                chat = model.start_chat(history=[])
                response = chat.send_message(initial_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"통신 오류 발생: {e}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍🚀" if message["role"] == "user" else "🕯️"):
            st.markdown(message["content"])

    if prompt := st.chat_input("당신의 이야기를 들려주세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(prompt)
        
        st.session_state.turn_count += 1
        
        with st.chat_message("assistant", avatar="🕯️"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Listening...")
            
            try:
                history = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
                
                final_instruction = ""
                if st.session_state.turn_count >= 5:
                    final_instruction = "\n\n(SYSTEM: 대화가 충분히 진행되었습니다. 이제 위 내용을 종합하여 [성좌 보고서]를 JSON으로 출력하고, 따뜻하게 인터뷰를 마무리하세요.)"
                
                chat = model.start_chat(history=history[:-1])
                response = chat.send_message(prompt + final_instruction)
                
                if "{" in response.text and "}" in response.text and "신뢰도" in response.text:
                    text_part = response.text.split("{")[0]
                    message_placeholder.markdown(text_part)
                    
                    try:
                        json_str = "{" + response.text.split("{", 1)[1] 
                        json_str = json_str.rsplit("}", 1)[0] + "}"
                        report_data = json.loads(json_str)
                        
                        st.balloons()
                        time.sleep(1)
                        
                        st.markdown(f"""
                        <div class='report-card'>
                            <h2 style='color:#FFD700; margin-bottom:10px;'>🏆 당신의 성좌 보고서</h2>
                            <h1 style='font-size: 2.5rem; margin: 20px 0;'>✨ {report_data.get('별자리명', '미지의 별')}</h1>
                            <p style='font-size: 1.2rem; color:#00D2FF;'><strong>핵심 가치:</strong> {report_data.get('핵심가치', '')}</p>
                            <hr style='border-color: rgba(255,215,0,0.3);'>
                            <p><strong>💰 수익화 모델:</strong> {report_data.get('수익화모델', '')}</p>
                            <p><strong>🔭 한줄평:</strong><br>"{report_data.get('한줄평', '')}"</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # [DB 저장 로직 실행]
                        with st.spinner("🚀 데이터를 별들의 도서관(DB)에 기록 중입니다..."):
                            is_saved = save_to_google_sheet(st.session_state.archetype, report_data, st.session_state.messages)
                        
                        if is_saved:
                            st.success("💾 당신의 별자리가 안전하게 기록되었습니다!")
                        else:
                            st.warning("⚠️ 기록 중 약간의 문제가 있었지만, 결과는 화면에 잘 나왔습니다.")

                        st.markdown("""
                        <div style='text-align: center; margin-top: 30px; padding: 20px;'>
                            <h3 style='font-family: serif; font-style: italic;'>
                            "오늘 발견한 빛은 당신의 시작일 뿐입니다.<br>
                            다음에 더 깊은 밤하늘에서 다시 만나요."
                            </h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.step = 4 
                        st.stop()
                        
                    except Exception as json_error:
                        message_placeholder.markdown(response.text)
                else:
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
            except Exception as e:
                message_placeholder.error(f"전송 오류: {e}")