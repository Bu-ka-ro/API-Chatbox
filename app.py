import streamlit as st
import openai
from datetime import date
import datetime
from zoneinfo import ZoneInfo

# List of example timezones (expandable)
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

# Timezone selector
selected_tz = st.selectbox("Select a timezone to display current time:", timezones)

# Get current time in UTC
now_utc = datetime.datetime.now(datetime.timezone.utc)

# Convert to selected timezone
try:
    user_tz = ZoneInfo(selected_tz)
    now_local = now_utc.astimezone(user_tz)
    time_display = now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    st.write(f"🕒 Current time in **{selected_tz}**: **{time_display}**")
except Exception as e:
    st.error(f"Error loading timezone: {e}")

# Date string for system prompt
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

# Function to detect time-related prompts
def is_time_request(text):
    time_keywords = ["what time is it", "current time", "current timezone", "tell me the time", "what's the time"]
    return any(keyword in text.lower() for keyword in time_keywords)

# Handle submission
if submitted and user_input:
    if is_time_request(user_input):
        st.write(f"🕒 The current time in **{selected_tz}** is: **{time_display}**")
    else:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": f"T
