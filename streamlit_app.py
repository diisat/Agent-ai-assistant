# app.py
import streamlit as st
import json
from sales_agent import get_sales_response
from agent import get_response
import requests


# Streamlit page config
st.set_page_config(page_title="AI Business Assistant", page_icon="🤖", layout="centered")

SIDEBAR_COLOR = "#8B5CF6"  # Purple
BACKGROUND_COLOR = "#f0f2f6"  # Light grey background

# Custom CSS styling
st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {BACKGROUND_COLOR}; }}
        [data-testid="stSidebar"] {{ background: {SIDEBAR_COLOR}; color: white; }}
        [data-testid="stSidebar"] * {{ color: white !important; }}
        .main-header {{
            text-align:center;
            padding:1.2rem;
            border-radius:12px;
            background: linear-gradient(90deg,#6EE7B7,#3B82F6);
            color:white;
            font-size:1.5rem;
            font-weight:bold;
            margin-bottom:1rem;
        }}
        .stChatMessage-user {{ background-color: #ffffff !important; border-radius:12px; padding:0.8rem; }}
        .stChatMessage-assistant {{ background-color: #e5e7eb !important; border-radius:12px; padding:0.8rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=100)
    st.markdown("## 🤖 AI Business Assistant")
    st.markdown("Choose your assistant")
    assistant_type = st.radio("Select Assistant", ["Marketing Assistant", "Sales Assistant"])
    st.markdown("---")
    st.markdown("💡 *Marketing Assistant* helps with campaigns & strategy.")
    st.markdown("🛒 *Sales Assistant* helps with products, stock & checkout.")

# Header
header_text = "💡 Your Creative Marketing Partner" if assistant_type == "Marketing Assistant" else "🛒 Your Smart Sales Partner"
st.markdown(f'<div class="main-header">{header_text}</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Display formatted assistant JSON when available
        if msg["role"] == "assistant" and isinstance(msg["content"], dict):
            st.json(msg["content"])
        else:
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about marketing ideas or sales products..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Choose which assistant to call
    with st.chat_message("assistant"):
        st.markdown("**🤖 Processing your request...**")
        if assistant_type == "Marketing Assistant":
            response_json = get_response(prompt)
            #response = requests.get(f"http://localhost:8000/sales/{prompt}")
            #response_json = response.json().get("response", "{}")
        else:
            response_json = get_sales_response(prompt)
            #response = requests.get(f"http://localhost:8000/sales/{prompt}")
            #response_json = response.json().get("response", "{}")

        try:
            parsed_response = json.loads(response_json)
            st.json(parsed_response)
            st.session_state.messages.append({"role": "assistant", "content": parsed_response})
        except json.JSONDecodeError:
            st.markdown(response_json)
            st.session_state.messages.append({"role": "assistant", "content": response_json})