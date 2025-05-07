import streamlit as st
import openai
import datetime
from datetime import date
from zoneinfo import ZoneInfo
import time

# Page setup
st.set_page_config(page_title="AI Chatbot with Timezone Clock", layout="centered")

# Title
st.title("🕒 AI Chatbot with Real-Time Clock")

# List of common timezones
timezones = [
    "UTC",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Asia/Kolkata",
    "Australia/Sydney"
]

# Select timezone
selected_tz = st.selectbox("Select a timezone:", timezones)

# Real-time clock display
clock_placeholder = st.empty()

def update_clock():
    while True:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        try:
            user_tz = ZoneInfo(selected_tz)
            now_local = now_utc.astimezone(user_tz)
            time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            clock_placeholder.markdown(f"### 🕐 Current time in **{selected_tz}**: `{time_display}`")
        except Exception as e:
            clock_placeholder.error(f"Error: {e}")
        time.sleep(1)

# Run clock in a separate thread so Streamlit doesn't freeze
import threading
if "clock_thread_started" not in st.session_state:
    st.session_state.clock_thread_started = True
    threading.Thread(target=update_clock, daemon=True).start()

# Chat input
st.subheader("💬 Chat with AI")
with st.form("chat_form"):
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")

# Detect if user is asking for time
def is_time_request(text):
    time_keywords = [
        "what time is it", "current time", "local time",
        "what's the time", "time now", "timezone", "current timezone"
    ]
    return any(kw in text.lower() for kw in time_keywords)

# Today's date
today = date.today().strftime("%A, %B %d, %Y")

# Set up OpenRouter
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

# Chat logic
if submitted and user_input:
    if is_time_request(user_input):
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        user_tz = ZoneInfo(selected_tz)
        now_local = now_utc.astimezone(user_tz)
        time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        st.write(f"🕒 The current time in **{selected_tz}** is: **{time_display}**")
    else:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": f"Today’s date is {today}. You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        st.write("🤖 Bot:", response.choices[0].message.content)
