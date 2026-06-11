import streamlit as st
import requests
from datetime import datetime
import base64

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="✨", layout="wide")

st.markdown("""
<style>
    /* Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default padding */
    .main > div {
        padding: 0rem 1rem;
    }
    
    /* Hide default header */
    header {
        background: transparent !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
        padding: 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Remove button full width */
    .stButton button {
        width: auto !important;
        min-width: 100px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Chat input styling */
    .stTextArea textarea {
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        font-size: 0.9rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 12px;
    }
    
    /* Message bubbles - modern */
    .user-msg {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-right-radius: 4px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .ai-msg {
        background: #f1f5f9;
        color: #1e293b;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-left-radius: 4px;
        margin: 8px 0;
        max-width: 80%;
    }
    
    /* Header modern */
    .main-header {
        text-align: left;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .main-header p {
        color: #64748b;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Chat container */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem 0;
    }
    
    /* Divider */
    hr {
        margin: 1rem 0;
        background: #e2e8f0;
    }
    
    /* Sidebar title */
    .sidebar-title {
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        margin-bottom: 1rem;
    }
    
    /* Quick topic buttons */
    .topic-btn {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        margin: 0.25rem;
    }
    
    .topic-btn:hover {
        background: rgba(255,255,255,0.2);
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
        padding: 1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>✨ AI Study Buddy</h1>
    <p>Your personal AI teacher — learn anything, anytime</p>
</div>
""", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

def ask_ai(question, mode):
    if mode == "Simple":
        prompt = "Explain like the student is 5 years old. Very simple words. Short sentences."
    elif mode == "Detailed":
        prompt = "Explain in detail with examples."
    else:
        prompt = "Explain clearly and simply."
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def download_chat():
    chat_text = f"AI Study Buddy Chat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for msg in st.session_state.chat:
        chat_text += f"You: {msg['q']}\n\nAI: {msg['a']}\n\n{'='*50}\n\n"
    return chat_text

with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚡ Settings</div>", unsafe_allow_html=True)
    mode = st.selectbox("Mode", ["Normal", "Simple", "Detailed"], label_visibility="collapsed")
    
    st.markdown("<div class='sidebar-title' style='margin-top: 2rem;'>📚 Quick Topics</div>", unsafe_allow_html=True)
    
    topics = ["🐍 Python", "🤖 AI", "🧮 Math", "🔬 Science", "🌍 History", "💻 Code", "🎨 Design", "📊 Data"]
    
    for i in range(0, len(topics), 2):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(topics[i], key=f"topic_{i}", use_container_width=False):
                with st.spinner("✨"):
                    answer = ask_ai(f"Explain {topics[i]} in simple words", mode)
                    st.session_state.chat.append({"q": f"Tell me about {topics[i]}", "a": answer, "time": datetime.now().strftime("%H:%M")})
                    st.rerun()
        with col2:
            if i+1 < len(topics):
                if st.button(topics[i+1], key=f"topic_{i+1}", use_container_width=False):
                    with st.spinner("✨"):
                        answer = ask_ai(f"Explain {topics[i+1]} in simple words", mode)
                        st.session_state.chat.append({"q": f"Tell me about {topics[i+1]}", "a": answer, "time": datetime.now().strftime("%H:%M")})
                        st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=False):
        st.session_state.chat = []
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask anything")
    user_input = st.text_area("", height=80, placeholder="e.g., What is machine learning? Explain quantum computing...", label_visibility="collapsed")
    
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("✨ Ask", use_container_width=False) and user_input:
            with st.spinner(""):
                answer = ask_ai(user_input, mode)
                st.session_state.chat.append({"q": user_input, "a": answer, "time": datetime.now().strftime("%H:%M")})
                st.rerun()

with col2:
    st.markdown("### 📝 Quiz")
    quiz_topic = st.text_input("", placeholder="Topic for quiz...", label_visibility="collapsed")
    if st.button("🎯 Generate Quiz", use_container_width=False) and quiz_topic:
        with st.spinner("Creating quiz..."):
            prompt = f"Generate 5 multiple choice questions about {quiz_topic}. Format: 1. Question\nA) Option\nB) Option\nC) Option\nD) Option\nAnswer: X"
            data = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]}
            response = requests.post(url, json=data, headers=headers)
            quiz_raw = response.json()["choices"][0]["message"]["content"]
            
            st.session_state.quiz_questions = []
            lines = quiz_raw.split('\n')
            current_q = {}
            for line in lines:
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    if current_q:
                        st.session_state.quiz_questions.append(current_q)
                    current_q = {'question': line, 'options': []}
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    if current_q:
                        current_q['options'].append(line)
                elif line.startswith('Answer:'):
                    if current_q:
                        current_q['answer'] = line.split(':')[1].strip()
            if current_q:
                st.session_state.quiz_questions.append(current_q)
            st.rerun()

st.markdown("---")

if len(st.session_state.chat) == 0:
    st.info("✨ Start a conversation — ask me anything!")

for item in reversed(st.session_state.chat[-15:]):
    st.markdown(f'<div class="user-msg"><strong>You</strong><br>{item["q"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-msg"><strong>AI Teacher</strong><br>{item["a"]}</div>', unsafe_allow_html=True)

if st.session_state.quiz_questions:
    st.markdown("---")
    st.markdown("### 📋 Quiz")
    for i, q in enumerate(st.session_state.quiz_questions):
        with st.expander(f"Q{i+1}: {q['question'][:60]}..."):
            st.markdown(q['question'])
            for opt in q.get('options', []):
                st.write(opt)
            if q.get('answer'):
                st.info(f"✅ Answer: {q['answer']}")
    
    if st.button("🗑️ Clear Quiz", use_container_width=False):
        st.session_state.quiz_questions = []
        st.rerun()

col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Export Chat", use_container_width=False) and st.session_state.chat:
        chat_content = download_chat()
        b64 = base64.b64encode(chat_content.encode()).decode()
        st.markdown(f'<a href="data:text/plain;base64,{b64}" download="chat.txt" style="text-decoration:none;">📁 Download</a>', unsafe_allow_html=True)
with col2:
    if st.button("🎲 Random Topic", use_container_width=False):
        topics_list = ["Python", "AI", "Space", "Ocean", "Animals", "Music", "Art", "Sports"]
        import random
        rand_topic = random.choice(topics_list)
        with st.spinner("✨"):
            answer = ask_ai(f"Explain {rand_topic} in simple words", mode)
            st.session_state.chat.append({"q": f"Tell me about {rand_topic}", "a": answer, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

st.markdown("""
<div class="footer">
    ✨ Made with Mistral AI — Learn something new today
</div>
""", unsafe_allow_html=True)