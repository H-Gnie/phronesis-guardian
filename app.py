import streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# [설정] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Celestial Navigator",
    page_icon="🌌",
    layout="wide"
)

# ---------------------------------------------------------
# [스타일] CSS: Deep Navy & Gold (Celestial Mood)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: radial-gradient(circle at center, #1B2735 0%, #090A0F 100%);
        color: #E6F1FF;
    }
    
    /* 텍스트 스타일 */
    h1, h2, h3 {
        color: #F6E05E !important;
        text-shadow: 0 0 15px rgba(246, 224, 94, 0.6);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 시나리오 박스 */
    .scenario-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(246, 224, 94, 0.3);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        font-size: 20px;
        line-height: 1.8;
        color: #E6F1FF;
        text-align: center;
    }

    /* 버튼 스타일: 감각적인 텍스트 강조 */
    .stButton>button {
        width: 100%;
        height: 120px;
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
        color: #F6E05E;
        border: 1px solid rgba(246, 224, 94, 0.3);
        border-radius: 20px;
        font-size: 22px;
        font-weight: 500;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .stButton>button:hover {
        background: rgba(246, 224, 94, 0.1);
        border-color: #F6E05E;
        color: #FFF;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 20px rgba(246, 224, 94, 0.4);
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

# ---------------------------------------------------------
# [연결] Gemini API
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    # 개발용 예외처리
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

progress_value = 33 if st.session_state.step == 1 else (66 if st.session_state.step == 2 else 100)
st.progress(progress_value, text=f"항해 진행률: {progress_value}%")

st.divider()

# ---------------------------------------------------------
# [Phase 1] 정체성 탐색 - 블라인드 선택
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown("""
    <div class='scenario-box'>
        "눈을 감고 상상해 보세요.<br>
        당신은 지금 낯선 행성의 한가운데 서 있습니다.<br>
        어디선가 바람이 불어오고, <b>가장 먼저 당신의 감각을 자극하는 것</b>은 무엇입니까?"
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗣️ 시끌벅적한 사람들의\n외침과 열기"):
            st.toast("✨ 무의식의 흐름을 따라 이동합니다...", icon="🚀")
            time.sleep(0.5)
            st.session_state.archetype["loc"] = "시장"
            st.session_state.archetype["loc_desc"] = "연결과 소통"
            st.session_state.step = 2
            st.rerun()
            
        if st.button("📖 오래된 종이 냄새와\n무거운 정적"):
            st.toast("✨ 무의식의 흐름을 따라 이동합니다...", icon="🚀")
            time.sleep(0.5)
            st.session_state.archetype["loc"] = "도서관"
            st.session_state.archetype["loc_desc"] = "시스템과 철학"
            st.session_state.step = 2
            st.rerun()
            
    with col2:
        if st.button("🍲 갓 구운 빵 냄새와\n따스한 온기"):
            st.toast("✨ 무의식의 흐름을 따라 이동합니다...", icon="🚀")
            time.sleep(0.5)
            st.session_state.archetype["loc"] = "주거지"
            st.session_state.archetype["loc_desc"] = "공감과 디테일"
            st.session_state.step = 2
            st.rerun()
            
        if st.button("🔨 날카로운 금속 소리와\n뜨거운 불꽃"):
            st.toast("✨ 무의식의 흐름을 따라 이동합니다...", icon="🚀")
            time.sleep(0.5)
            st.session_state.archetype["loc"] = "공방"
            st.session_state.archetype["loc_desc"] = "문제해결과 기술"
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# [Phase 2] 도구 발견 - 블라인드 선택
# ---------------------------------------------------------
elif st.session_state.step == 2:
    loc_name = st.session_state.archetype['loc']
    
    bridge_texts = {
        "시장": "소음과 열기를 선택한 당신은, <b>흐름과 변화</b>를 두려워하지 않는 모험가입니다.<br>이제 그 혼란 속에서 살아남기 위해 본능적으로 집어 든 물건이 있습니다.",
        "도서관": "정적과 지식을 선택한 당신은, <b>본질과 이치</b>를 탐구하는 현자입니다.<br>이제 그 깊은 사유를 완성하기 위해 본능적으로 집어 든 물건이 있습니다.",
        "주거지": "온기와 냄새를 선택한 당신은, <b>사람과 마음</b>을 먼저 살피는 치유자입니다.<br>이제 그 소중한 것들을 지키기 위해 본능적으로 집어 든 물건이 있습니다.",
        "공방": "불꽃과 소리를 선택한 당신은, <b>변화와 창조</b>를 즐기는 혁명가입니다.<br>이제 무언가를 만들어내기 위해 본능적으로 집어 든 물건이 있습니다."
    }
    current_bridge = bridge_texts.get(loc_name, "당신의 무의식이 이끄는 곳에 도착했습니다.")

    st.markdown(f"""
    <div class='scenario-box'>
        "{current_bridge}<br><br>
        낡은 가방 안에는 네 가지 물건이 들어있습니다.<br>
        무엇인지 확인하지 않고, <b>손끝에 닿는 촉감만으로</b> 하나를 꺼냅니다."
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 차갑고 매끄러운\n유리 렌즈"):
            st.toast("💫 운명의 파편을 획득했습니다!", icon="✨")
            time.sleep(0.5)
            st.session_state.archetype["tool"] = "돋보기"
            st.session_state.archetype["tool_desc"] = "데이터와 분석"
            st.session_state.step = 3
            st.rerun()
            
        if st.button("🧭 끊임없이 흔들리는\n가느다란 바늘"):
            st.toast("💫 운명의 파편을 획득했습니다!", icon="✨")
            time.sleep(0.5)
            st.session_state.archetype["tool"] = "나침반"
            st.session_state.archetype["tool_desc"] = "전략과 기획"
            st.session_state.step = 3
            st.rerun()
            
    with col2:
        if st.button("✒️ 끝이 뾰족하고 가벼운\n새의 깃털"):
            st.toast("💫 운명의 파편을 획득했습니다!", icon="✨")
            time.sleep(0.5)
            st.session_state.archetype["tool"] = "깃펜"
            st.session_state.archetype["tool_desc"] = "브랜딩과 마케팅"
            st.session_state.step = 3
            st.rerun()
            
        if st.button("🔧 묵직하고 기름때 묻은\n쇠막대"):
            st.toast("💫 운명의 파편을 획득했습니다!", icon="✨")
            time.sleep(0.5)
            st.session_state.archetype["tool"] = "수리도구"
            st.session_state.archetype["tool_desc"] = "최적화와 실행"
            st.session_state.step = 3
            st.rerun()

# ---------------------------------------------------------
# [Phase 3] 가치 증명 - 감정의 거울 (v1.5 로직 적용)
# ---------------------------------------------------------
elif st.session_state.step == 3:
    if not st.session_state.messages:
        loc = st.session_state.archetype['loc']
        tool = st.session_state.archetype['tool']
        
        # [수정됨] v1.5: '내면으로의 초대' - 평가가 아닌 공감으로 시작
        intro_text = f"""
        🕯️ **내면으로의 초대**
        
        당신은 본능적으로 **[{loc}]**으로 향했고, 손에 **[{tool}]**을 쥐었습니다.
        
        이 선택은 우연이 아닙니다. 당신의 무의식이 그곳에서 무언가를 느꼈기 때문입니다.
        이제, 그 선택 뒤에 숨겨진 당신의 진짜 마음을 들여다보겠습니다.
        """
        st.info(intro_text, icon="🕯️")
        
        # [수정됨] AI에게 보내는 첫 지령: '감정 코칭'과 '거울 기법' 지시
        initial_prompt = f"""
        사용자는 [{loc}]을 선택했고, [{tool}]을 집어들었어.
        
        [대화의 대원칙]에 따라 대화를 시작해줘.
        1. 사용자의 선택을 비난하거나 평가하지 마.
        2. 그 선택을 했을 때 **'어떤 기분(How it felt)'**이었는지 조심스럽게 물어봐.
        3. 정답을 맞히려고 하지 말고, 사용자의 내면을 비추는 거울처럼 행동해.
        
        첫 마디 예시: "그 시끄러운 시장 속에서 차가운 렌즈를 쥐었을 때, 어떤 마음이 드셨나요? 불안함이었나요, 아니면 호기심이었나요?"
        """
        
        try:
            with st.spinner("별자리 안내자가 당신의 마음을 읽고 있습니다..."):
                chat = model.start_chat(history=[])
                response = chat.send_message(initial_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"통신 오류 발생: {e}")

    st.markdown("### 🗣️ 심층 대화: 당신의 마음을 이야기해주세요")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍🚀" if message["role"] == "user" else "🕯️"):
            st.markdown(message["content"])

    if prompt := st.chat_input("그때의 기분, 혹은 떠오르는 기억을 적어주세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🕯️"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Listening...")
            
            try:
                history = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=history[:-1]) 
                response = chat.send_message(prompt) 
                
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
                # 결과(JSON) 감지
                if "{" in response.text and "}" in response.text and "신뢰도" in response.text:
                    st.balloons()
                    st.success("✨ 당신이라는 우주가 발견되었습니다.", icon="🌌")
                    
            except Exception as e:
                message_placeholder.error(f"전송 오류: {e}")