import streamlit as st
import openai
import datetime
from datetime import date, timezone  # Added timezone
from zoneinfo import ZoneInfo

# Set up OpenRouter API
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

# App styling
st.set_page_config(page_title="AI Chatbot", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #e0f8f8;
    }
    .chatbox {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title("🤖 AI Chatbot")

# Personality selection
st.subheader("🎭 Choose Chatbot Personality")
personalities = {
    "Friendly": "You are a friendly, upbeat assistant who answers like a casual conversation with a friend.",
    "Professional": "You are a formal assistant who provides concise and factual answers with a professional tone.",
    "Sarcastic": "You are a sarcastic assistant who answers with humor and irony, but still provides correct information.",
    "Einstein": "You are speaking as if you're Albert Einstein, using analogies and insights inspired by your scientific background.",
    "Motivator": "You are a motivating life coach who inspires the user with every answer, encouraging positive thinking."
}
selected_persona = st.selectbox("Select a personality:", list(personalities.keys()))

# Chat input section
st.subheader("💬 Chat with the Bot")
with st.form("chat_form"):
    st.markdown('<div class="chatbox">', unsafe_allow_html=True)
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")
    st.markdown('</div>', unsafe_allow_html=True)

# Timezone selection below chat
st.subheader("🕒 Timezone Info")
timezones = [
    "UTC", "America/New_York", "America/Los_Angeles",
    "Europe/London", "Europe/Paris", "Asia/Tokyo",
    "Asia/Kolkata", "Australia/Sydney", "Asia/Manila"
]
selected_tz = st.selectbox("Select a timezone to display current time:", timezones)

# Get current time in selected timezone
now_utc = datetime.datetime.now(timezone.utc)
try:
    user_tz = ZoneInfo(selected_tz)
    now_local = now_utc.astimezone(user_tz)
    time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
except Exception as e:
    st.error(f"Error loading timezone: {e}")
    time_display = "Unknown Time"

# Detect time-related user input
def is_time_request(text):
    time_keywords = [
        "what time is it", "current time", "local time",
        "what's the time", "time now", "timezone", "current timezone"
    ]
    return any(kw in text.lower() for kw in time_keywords)

# Handle chat responses
if submitted and user_input:
    if is_time_request(user_input):
        st.write(f"🕒 The current time in **{selected_tz}** is: **{time_display}**")
    else:
        system_prompt = f"Today’s date and time is {time_display}. {personalities[selected_persona]}"
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        st.write("🤖 Bot:", response.choices[0].message.content)

# Display time info again
st.write(f"🕒 Current time in **{selected_tz}**: **{time_display}**")
