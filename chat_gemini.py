# Importing libraries
import time
import random
import streamlit as st
import google.generativeai as genai
from click import prompt
from streamlit import session_state

# Website Settings
st.set_page_config(
    page_title="Ana",
    page_icon=":mom:"
)

# Title
st.title("Ana 👑")
st.caption("Chatbot created with Gemini Pro")

# To put API Key in the website
if "api_key" not in st.session_state:
    api_key = st.sidebar.text_input("API Key", type="password")
    if api_key.startswith("AI"):
        st.session_state.api_key = api_key
        genai.configure(api_key=session_state.api_key)
        st.sidebar.success("API key is valid!", icon= "✅")
    else:
        st.sidebar.warning("Please, inform the API key.", icon= "⚠️")

# Create a conversation historic
if "historic" not in st.session_state:
    st.session_state.historic = []

# Create a historic model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create the chat
chat = model.start_chat(history=st.session_state.historic)

# Cleaning the conversation
with st.sidebar:
    if st.button("Clean the chat", type="primary", use_container_width=True):
        st.session_state.historic = []
        st.rerun()

# Getting the historic messages
for message in chat.history:
    if message.role == "model":
        role = "assistant"
    else:
        role = message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Checking if the API key was informed to create the chat
if "api_key" in st.session_state:
    prompt = st.chat_input("Type your prompt here...")
    if prompt:
        prompt = prompt.replace("\n", "\n")

        # Write the user opening
        with st.chat_message("user"):
            st.markdown(prompt)
        # Write the Gemini message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("I'm thinking...")

            # Check if there is not error in the users entrance
            try:
                # Write the Gemini answer letter by letter
                answer = ""
                for chunck in chat.send_message(prompt, stream=True):
                    words_count = 0
                    random_number = random.randint(5, 10)
                    for word in chunck.text:
                        answer += word
                        words_count +=1
                        # Typiyng like a typiyng machine
                        if words_count == random_number:
                            time.sleep(0.05)
                            message_placeholder.markdown(answer + " ")
                            words_count = 0
                            random_number = random.randint(5, 10)
                message_placeholder.markdown(answer)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.historic = chat.history
