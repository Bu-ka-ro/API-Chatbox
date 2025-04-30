import streamlit as st
import openai
from datetime import date

# Get today's date (string)
today = date.today().strftime("%A, %B %d, %Y")

# OpenRouter API base and key
openai.api_base = "https://urldefense.com/v3/__https://openrouter.ai/api/v1__;!!HoV-yHU!o1sByG5mCjTnTzM65djuMN5gF0ObG0WlJ36aOe2tkFM0XQDTnL9u0vfkyfSv3N70tFKusTkIC64tC_Ohp8IuPJgfcHc$ "
openai.api_key = st.secrets["openrouter_key"]

st.title("AI Chatbot")

# Code for input form
with st.form("chat_form"):
    user_input = st.text_input("Ask anything:")
    submitted = st.form_submit_button("Get Response")

if submitted and user_input:
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct:free",  # Free model ID
        messages=[
            {"role": "system", "content": f"Today’s date is {today}. You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    st.write("Bot:", response.choices[0].message["content"])
