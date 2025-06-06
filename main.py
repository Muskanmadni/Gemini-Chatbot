import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load API key from environment
load_dotenv()
openrouter_api_key = os.getenv("OpenRouter_key")

# Set Streamlit page config
st.set_page_config(page_title="Gemini Chatbot (via OpenRouter)", page_icon="🤖", layout="centered")

# 💾 Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input" not in st.session_state:
    st.session_state.input = ""

# 🎨 Custom CSS
st.markdown("""
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }
    .stApp {
        background: rgba(0, 0, 0, 0.6);
        color: white;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
    }
    .chat-message {
        padding: 10px 14px;
        border-radius: 14px;
        max-width: 75%;
        word-wrap: break-word;
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.5s forwards;
    }
    .user {
        background-color: #DCF8C6;
        align-self: flex-end;
        margin-left: auto;
        color: black;
    }
    .bot {
        background-color: #F1F0F0;
        align-self: flex-start;
        margin-right: auto;
        color: black;
    }
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 15px;
        align-items: center;
    }
    .input-container input[type="text"] {
        flex: 1;
        padding: 10px;
        border-radius: 20px;
        border: 1px solid #555;
        background-color: #333;
        color: white;
        outline: none;
    }
    .input-container input[type="text"]::placeholder {
        color: #aaa;
    }
    .input-container button {
        background-color: #444;
        border: none;
        border-radius: 50%;
        padding: 10px;
        cursor: pointer;
        transition: transform 0.2s, background-color 0.2s;
    }
    .input-container button:hover {
        background-color: #666;
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 OpenRouter Gemini API call
def generate_gemini_response(user_input):
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.5-flash-preview-05-20",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 1000
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# 📜 Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, (sender, message) in enumerate(st.session_state.chat_history):
    sender_class = "user" if sender == "You" else "bot"
    st.markdown(
        f'<div class="chat-message {sender_class}" style="animation-delay: {i*0.1}s;"><b>{sender}:</b> {message}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ✉️ Handle send button
def handle_send():
    user_input = st.session_state.input.strip()
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        response_text = generate_gemini_response(user_input)
        st.session_state.chat_history.append(("Gemini", response_text))
        st.session_state.input = ""

# 💬 Input box and send button
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    st.text_input("Type your message...", key="input", placeholder="Ask anything...", label_visibility="collapsed")
with col2:
    st.button("▶️", on_click=handle_send)
st.markdown('</div>', unsafe_allow_html=True)
