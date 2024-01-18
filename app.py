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

if rol == "Code Generator 🔧":
    lang = st.sidebar.text_input("Language / Software 📝","python")

    want = st.sidebar.selectbox("you want ℹ️",['Generate only code','Generate code with explanation ','Generate 3 different codes','Generate code with error handling','Generate code (shortest as possible)'])

    tone = st.sidebar.selectbox("Tone 🤝",["Friendly and helpful","Professional","Humorous and entertaining","Sarcastic and witty","Formal and academic"]) 

    # out_len = st.sidebar.text_input("Output content Language 🌐:","english")

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

def main_pr(rol,qu):
    if rol == "Code Generator 🔧":
        main_prompt = f"I want you to act as a code generator in {lang}. I will give you a description of the program I want,along with a command {want} and a desired tone {tone}. you will generate a {lang} program, code, or script. The program should be efficient, readable, and well-commented. The program should also run without errors.  My first request is a program that {prompt}." 
        
    elif rol =="Act as a Code Review Helper 👀":
        main_prompt = f"I want you to act as a code review helper for me. I will give you code snippets, and you will only write your feedback on style, best practices, and code smells. The feedback should be descriptive rather than judgmental and include suggestions for improvement. It should only be about the given code snippet, not related to the whole project or other parts of the code. The feedback should not be a list of issues, but a cohesive review comment. My first code snippet is: {qu}"
    
    elif rol =="Act as a Code Error Solver Assistant ❌":
        main_prompt = f'''
                        I want you to act as an assistant to help me solve code errors. I will provide you with the following information:

                            Error message (if available)
                            Code snippet (if available)
                            Additional context (if available)

                        I need you to provide me with the following information:

                            The most likely cause of the error
                            Provide a list of possible solutions to fix the error
                            Help me understand the error message (if provided)
                            Provide a code sample that demonstrates the error and how to fix it (if no code snippet is provided)

                        Please respond in a concise and clear manner. Do not use technical jargon or complex explanations. The code examples should be in Python, and the error messages should be in English.
                        My first request {qu}
                        '''
    return main_prompt

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
            
            main_prompt = main_pr(rol,prompt)
            
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
