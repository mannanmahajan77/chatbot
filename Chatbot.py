import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def load_training_data():
    with open('training_data.json', 'r') as f:
        return json.load(f)

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def handle_support_interaction(question):
    if "order status" in question.lower():
        return "Please provide your order number to check the status."
    elif "account issue" in question.lower():
        return "Can you describe the issue with your account?"
    elif "product information" in question.lower():
        return "Which product would you like information about?"
    else:
        response = get_gemini_response(question)
        return response

def main():
    st.set_page_config(page_title="ChatBot")
    st.header("ChatBot")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input("Input:", key='input')
    submit = st.button("Ask me anything")

    if submit and input_text:
        st.session_state['chat_history'].append(("You", input_text))
        response = handle_support_interaction(input_text)

        if isinstance(response, str):
            st.session_state['chat_history'].append(("Bot", response))
            st.write(response)
        else:
            st.subheader("The Response is")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

    st.subheader("The Chat history is")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
