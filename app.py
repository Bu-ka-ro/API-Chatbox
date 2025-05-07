import streamlit as st
import openai
from datetime import date

from zoneinfo import ZoneInfo
    
    # Get current time in UTC
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    
    # Define the target timezone
    timezone_Newyork = ZoneInfo("USA/Newyork")
    
    # Convert UTC time to the target timezone
    now_tokyo = now_utc.astimezone(timezone_newyork)
    
     print("Current time in UTC:", now_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    print("Current time in newyork:", now_newyork.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

today = date.today().strftime("%A, %B %d, %Y")

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["openrouter_key"]

st.title("AI Chatbot")

with st.form("chat_form"):
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")

if submitted and user_input:
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {"role": "system", "content": f"Today’s date is {today}. You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    st.write("Bot:", response.choices[0].message.content)
