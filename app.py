import streamlit as st
import openai
import datetime
from datetime import date
from zoneinfo import ZoneInfo

# Set up OpenRouter API
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

# Custom CSS for background and chatbox styling
st.markdown("""
    <style>
        body {
            background-color: #e0f8f8;
        }
        .chat-box {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .chat-box input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🤖 AI Chatbot")

# Personality selection
st.subheader("Choose Chatbot Personality")
personalities = {
    "Friendly": "You are a friendly, upbeat assistant who answers like a casual conversation with a friend.",
    "Professional": "You are a formal assistant who provides concise and factual answers with a professional tone.",
    "Sarcastic": "You are a sarcastic assistant who answers with humor and irony, but still provides correct information.",
    "Einstein": "You are speaking as if you're Albert Einstein, using analogies and insights inspired by your scientific background.",
    "Motivator": "You are a motivating life coach who inspires the user with every answer, encouraging positive thinking."
}
selected_persona = st.selectbox("Select a personality:", list(personalities.keys()))

# Input form in a custom chatbox container
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)  # Start chatbox container
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")
    st.markdown('</div>', unsafe_allow_html=True)  # End chatbox container

# Today's date
today = date.today().strftime("%A, %B %d, %Y")

# Detect if the user is asking for the time
def is_time_request(text):
    time_keywords = [
        "what time is it", "current time", "local time", 
        "what's the time", "time now", "timezone", "current timezone"
    ]
    return any(kw in text.lower() for kw in time_keywords)

# Chat logic
if submitted and user_input:
    if is_time_request(user_input):
        st.session_state.show_time = True  # Trigger time display
    else:
        # Corrected indentation: both the time and system prompt inside the else block
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        system_prompt = f"Today’s date and time is {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')}. {personalities[selected_persona]}"

        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        st.write("🤖 Bot:", response.choices[0].message.content)

# Timezone selection placed after chat
st.subheader("🕒 Timezone Info")
timezones = [
    "UTC", "America/New_York", "America/Los_Angeles",
    "Europe/London", "Europe/Paris", "Asia/Tokyo",
    "Asia/Kolkata", "Australia/Sydney", "Asia/Manila"
]
selected_tz = st.selectbox("Select a timezone to display current time:", timezones)

# Show time based on timezone
now_utc = datetime.datetime.now(datetime.timezone.utc)
try:
    user_tz = ZoneInfo(selected_tz)
    now_local = now_utc.astimezone(user_tz)
    time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    st.write(f"🕒 Current time in **{selected_tz}**: **{time_display}**")
except Exception as e:
    st.error(f"Error loading timezone: {e}")
