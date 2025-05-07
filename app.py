import streamlit as st
import openai
from datetime import date
import datetime
from zoneinfo import ZoneInfo

# Get current time in UTC
now_utc = datetime.datetime.now(datetime.timezone.utc)

# Define the target timezone
timezone_Newyork = ZoneInfo("America/New_York")

# Convert UTC time to the target timezone
now_newyork = now_utc.astimezone(timezone_Newyork)

# Format times
utc_time_str = now_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')
ny_time_str = now_newyork.strftime('%Y-%m-%d %H:%M:%S %Z%z')

today = date.today().strftime("%A, %B %d, %Y")

# Set OpenRouter API credentials
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

# App UI
st.title("AI Chatbot")

# Show current time in New York
st.write(f"🕒 Current time in New York: **{ny_time_str}**")

# Input form
with st.form("chat_form"):
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")

# Chat response
if submitted and user_input:
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {"role": "system", "content": f"Today’s date is {today}. You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    st.write("🤖 Bot:", response.choices[0].message.content)
