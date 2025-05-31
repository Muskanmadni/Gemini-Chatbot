import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("Gemini Chatbot with File Upload")

# 🌌 Custom CSS with background image + animations
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
        background: rgba(0,0,0,0.6);
        color: white;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        scrollbar-width: thin;
        scrollbar-color: #666 transparent;
    }
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #666;
        border-radius: 10px;
    }
    .chat-message {
        padding: 10px 14px;
        border-radius: 14px;
        max-width: 75%;
        word-wrap: break-word;
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.6s forwards;
    }
    .chat-message:hover {
        transform: scale(1.02);
        transition: transform 0.3s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
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
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 15px;
        align-items: center;
        opacity: 0;
        animation: fadeInSlide 1s forwards 0.3s;
    }
    @keyframes fadeInSlide {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .input-container input[type="text"] {
        flex: 1;
        padding: 10px;
        border-radius: 20px;
        border: 1px solid #555;
        background-color: #333;
        color: white;
        outline: none;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .input-container input[type="text"]:focus {
        border-color: #0f0;
        box-shadow: 0 0 8px #0f0;
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
        transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
    }
    .input-container button:hover {
        background-color: #666;
        transform: scale(1.1);
        box-shadow: 0 0 10px #888;
    }
    .input-container button:active {
        transform: scale(0.95);
    }
</style>

""", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input" not in st.session_state:
    st.session_state.input = ""

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# File uploader (optional)
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "pdf", "csv"])
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.session_state.uploaded_file = file_content

# Chat history with animations
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, (sender, message) in enumerate(st.session_state.chat_history):
    sender_class = "user" if sender == "You" else "bot"
    st.markdown(
        f'<div class="chat-message {sender_class}" style="animation-delay: {i*0.1}s;"><b>{sender}:</b> {message}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# Send handler
def handle_send():
    user_input = st.session_state.input
    file_text = st.session_state.uploaded_file or ""
    if user_input or file_text:
        combined_input = f"{user_input}\n\nFile content:\n{file_text}" if file_text else user_input
        st.session_state.chat_history.append(("You", user_input))
        response = model.generate_content(combined_input)
        response_text = response.text if hasattr(response, "text") else ""
        st.session_state.chat_history.append(("Gemini", response_text))
        st.session_state.input = ""

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    st.text_input("Type your message...", key="input", placeholder="Ask anything...", label_visibility="collapsed")
with col2:
    st.button("▶️", on_click=handle_send)
st.markdown('</div>', unsafe_allow_html=True)
