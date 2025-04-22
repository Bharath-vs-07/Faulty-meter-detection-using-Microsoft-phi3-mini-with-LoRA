import streamlit as st
import random
import time
import re
from datetime import datetime
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from responses import generate_response

# API Key for Google Generative AI
API_KEY = 'your-api-key'

# Custom CSS and JavaScript for enhanced visuals and effects
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Roboto', sans-serif;
            background-color: D3D3D3;
            color: #F5F5F5;
            margin: 0;
            padding: 0;
        }
        .stApp {
            background: linear-gradient(to bottom right, #0f0f0f, #2a2a2a);
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .title-container {
            text-align: center;
            margin-bottom: 25px;
        }
        h1 {
            color: white;
            font-weight: 700;
            font-size: 36px;
            margin: 0;
            border-right: 4px solid gray;
            white-space: nowrap;
            overflow: hidden;
            animation: typing 3.5s steps(40, end), fadeout 0.5s forwards 3.5s;
            display: inline-block;
        }
        .welcome-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .welcome-message {
            font-size: 10px;
            color: gray;
            white-space: nowrap;
            overflow:hidden;
            border-right: 2px solid lightgray;
            animation: typing-welcome 3.5s steps(10, end), fadeout-welcome 0.5s forwards 4s;
            display: inline-block;
        }
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        @keyframes typing-welcome {
            from { width: 0; }
            to { width: 100%; }
        }
        @keyframes fadeout {
            from { border-right-color: gray; }
            to { border-right-color: transparent; }
        }
        @keyframes fadeout-welcome {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        .message-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 80%;
            max-width: 800px;
            margin: 0 auto;
        }
        .message-row {
            display: flex;
            align-items: center;
        }
        .message-row.user {
            justify-content: flex-end;
        }
        .user-message {
            text-align: right;
            background-color: #555;
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            display: inline-block;
            max-width: 70%;
        }
        .assistant-message {
            text-align: left;
            background-color: #333;
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            display: inline-block;
            max-width: 70%;
        }
        .assistant-label {
            font-size: 14px;
            color: #888;
            text-align: left;
            margin-bottom: 5px;
            margin-top: 5px;
        }
        .sidebar {
            background-color: #2a2a2a;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const title = document.querySelector('h1');
            const welcomeMessage = document.querySelector('.welcome-message');

            title.style.width = '100%';
            welcomeMessage.style.width = '100%';

            function fadeOutWelcome() {
                welcomeMessage.classList.add('fadeout');
                setTimeout(() => {
                    welcomeMessage.style.display = 'none';
                }, 500);
            }

            setTimeout(fadeOutWelcome, 4000);
        });
    </script>
""", unsafe_allow_html=True)

# Title of the Webpage with Typing Effect
import streamlit as st

# Define HTML with inline CSS and media queries
st.markdown("""
    <style>
        /* Default styles */
        .title-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .title-container h1 {
            font-size: 24px;
            color: #00ff00;
        }
        
        /* Media query for tablets and smaller devices */
        @media (max-width: 768px) {
            .title-container h1 {
                font-size: 20px; /* Adjust font size for tablets */
            }
        }

        /* Media query for mobile devices */
        @media (max-width: 480px) {
            .title-container h1 {
                font-size: 20px; /* Adjust font size for mobile devices */
            }
        }
    </style>

    <div class='title-container'>
        <h1>Electricity Diagnosis Chatbot</h1>
    </div>
""", unsafe_allow_html=True)


# Welcome message that disappears after being fully typed


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=API_KEY)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input_processing(user_question, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

# Updated response generator function
def response_generator(response):
    response_text = ""
    for word in response.split():
        response_text += word + " "
        yield response_text
        time.sleep(0.1)  # Slightly increased delay for a more interactive feel

# Function to handle response generation
def get_response(user_input):
    
    # First try to get a response from the `responses` module
    response = generate_response(user_input.lower())
    
    # List of keywords to check
    keywords = ["issue", "trouble", "difficulty", "problem", "concern", "help","assistance"]
    
    # Check if any keyword is in the user input and handle the case
    if any(keyword in user_input.lower() for keyword in keywords) and not st.session_state.get('pdf_analysis', False):
        response = "Please upload the PDF document so I can help you with the problem."
    
    # If no response from `responses` module, use the LLM
    if response is None:
        response = user_input_processing(user_input, API_KEY)
    
    return response

# Main application logic
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def display_conversation():
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    for message in st.session_state.conversation_history:
        role, content = message["role"], message["content"]
        if role == "user":
            st.markdown(f'''
                <div class="message-row user">
                    <div class="user-message">{content}</div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="message-row">
                    <div class="assistant-label">Assistant</div>
                    <div class="assistant-message">{content}</div>
                </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

display_conversation()

# Handle user input
if user_input := st.chat_input("Your Queries?"):
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.markdown(f'''
        <div class="message-row user">
            <div class="user-message">{user_input}</div>
        </div>
    ''', unsafe_allow_html=True)

    assistant_response = get_response(user_input)
    response_container = st.empty()
    for response_part in response_generator(assistant_response):
        response_container.markdown(f'''
            <div class="message-row">
                <div class="assistant-label">Assistant</div>
                <div class="assistant-message">{response_part}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_response})
