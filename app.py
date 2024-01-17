from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import textwrap
import shelve
import google.generativeai as genai

def pre_p(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Check if the Google API key is provided
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("Google API key is missing. Please provide it in the .env file.")
    st.stop()

genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-pro')

# Initialize our Streamlit app
st.set_page_config(page_title="AI Generator", page_icon="🚀")

# Add some style and emojis
# st.subheader("How can I help you today? ❄️")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Sidebar for user to select the role of the chatbot
st.sidebar.subheader("Code with AI ☃️")

rol = st.sidebar.selectbox("Select Roll of model",['Code Generator 🔧','Act as a Code Review Helper 👀','Act as a Code Error Solver Assistant ❌'])

lang = st.sidebar.text_input("Language / Software 📝","python")

want = st.sidebar.selectbox("you want ℹ️",['Generate code with explanation ','Generate 3 different codes','Generate only code','Generate code with error handling','Generate code (shortest as possible)'])

tone = st.sidebar.selectbox("Tone 🤝",["Professional and informative","Humorous and entertaining","Sarcastic and witty","Friendly and helpful","Formal and academic"]) 

out_len = st.sidebar.text_input("Output content Language 🌐:","english")

st.subheader(f"{rol}❄️")

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "chat" not in st.session_state:
    chat = model.start_chat(history=[])
    st.session_state.chat = chat

# Initialize or load chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Your chat_ai function
def chat_ai(question):
    try:
        response = st.session_state.chat.send_message(question)
        response_text = response.text
    except Exception as e:
        try:
            response_text = f"{response.candidates[0].content.parts[0].text} 🫣"
        except:
            response_text = f"""Sorry, I not give you answer. 🫣 check question  !!!"""
    return response_text

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner("Generating response... 🔄"):
            main_prompt = f"I want you to act as a code generator in {lang}. I will give you a description of the program I want,along with a command {want} and a desired tone {tone}. you will generate a {lang} program, code, or script. The program should be efficient, readable, and well-commented. The program should also run without errors.  My first request is a program that {prompt}." 
            
            response = chat_ai(main_prompt)
            full_response += response
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(pre_p(full_response))
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)

# st.snow()


# code_generator_emoji = "🔧"
# code_review_helper_emoji = "👀"
# code_error_solver_emoji = "❌"

# generate_with_explanation_emoji = "ℹ️"
# generate_3_different_codes_emoji = "🔄"
# generate_only_code_emoji = "💻"
# generate_with_error_handling_emoji = "🚨"
# generate_shortest_code_emoji = "🚀"

# professional_and_informative_emoji = "👔💼"
# humorous_and_entertaining_emoji = "😄🎉"
# sarcastic_and_witty_emoji = "😏🔍"
# friendly_and_helpful_emoji = "🤝🆘"
# formal_and_academic_emoji = "🎓📚"
