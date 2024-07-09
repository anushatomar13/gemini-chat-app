from dotenv import load_dotenv
import streamlit as st
import os
import textwrap
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
       
        if response and hasattr(response, 'text'):
            return response.text
        else:
           
            if hasattr(response, 'candidate') and hasattr(response.candidate, 'safety_ratings'):
                print("Response blocked due to safety ratings:", response.candidate.safety_ratings)
            return "The response was blocked due to safety concerns."
    except ValueError as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating the response."


st.set_page_config(page_title="Peach - An AI powered chatbot")


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap');
    body {
        background-color: #000000;
        font-family: 'Oswald';
    }
    .main {
        color: #ffffff;
        background-color: #000000;
        border-radius: 10px;
        padding: 20px;
    }
    .stTextInput > div > div > input {
        border: 2px solid #ccc;
        border-radius: 5px;
        padding: 15px;
        font-size: 24px;
        color: #000000; /* Black color for input text */
        width: 100%;
        font-family: 'Oswald';
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        font-family: 'Roboto', sans-serif;
    }
    .stButton > button:hover {
        background-color: #ffffff;
        color: #4CAF50;
    }
    .stHeader {
        color: #ffffff !important;
        font-weight: bold !important;
        font-style: italic;
        font-size: 36px !important;
        font-family: 'Roboto', sans-serif !important;
    }
    .input-label {
        color: #ffffff;
        font-weight: bold;
        font-style: italic;
        font-size: 30px;
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="stHeader">Hey! I am Peach. Ask me anything! I would love to help you🐋</h1>', unsafe_allow_html=True)

st.markdown('<p class="input-label">Input:</p>', unsafe_allow_html=True)
input_text = st.text_input("", key="input")

submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    st.write(response)
