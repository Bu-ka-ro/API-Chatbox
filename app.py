import streamlit as st
import openai
from datetime import date
import datetime
from zoneinfo import ZoneInfo

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
    "Asia/Manila"
]

# Select timezone
selected_tz = st.selectbox("Select a timezone to display current time:", timezones)

# Get current time in UTC
now_utc = datetime.datetime.now(datetime.timezone.utc)

# Convert UTC to selected timezone
try:
    user_tz = ZoneInfo(selected_tz)
    now_local = now_utc.astimezone(user_tz)
    time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    st.write(f"🕒 Current time in **{selected_tz}**: **{time_display}**")
except Exception as e:
    st.error(f"Error loading timezone: {e}")

# Today's date for system prompt
today = date.today().strftime("%A, %B %d, %Y")

# OpenRouter setup
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

# App title
st.title("AI Chatbot")

# Input form
with st.form("chat_form"):
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")

# Detect if the user is asking for the time
def is_time_request(text):
    time_keywords = [
        "what time is it", "current time", "local time", "what's the time", "time now", "timezone", "current timezone"
    ]
    return any(kw in text.lower() for kw in time_keywords)

# Chat logic
if submitted and user_input:
    if is_time_request(user_input):
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
