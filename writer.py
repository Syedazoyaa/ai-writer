import streamlit as st
import os
import base64
import google.generativeai as genai

# Configure the Google Generative AI with your API key
genai.configure(api_key="AIzaSyDl2nIaYT9ef8vJ6NDhXnIOUj-Z_UmYfXU")  

# Set Streamlit app page configuration (must be first Streamlit command)
st.set_page_config(page_title="Writer.AI", layout="wide")

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])

# Function to set background image using base64 encoding
def set_background_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: Image file '{image_path}' not found.")
    except Exception as e:
        st.error(f"Error: {e}")

# Get the absolute path to the current directory
current_dir = os.path.dirname(__file__)

# Set background image (assuming "BABG.png" is in the same directory)
image_path = os.path.join(current_dir, "BABG.png")
set_background_image(image_path)

# Function to generate content using Gemini Pro model
def get_gemini_response(content_type, user_input):
    try:
        question = f"Generate a {content_type} on: {user_input} make it very evident that it's a {content_type} and also give the heading as 'BLOG ON {user_input}'"
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")

# Main content
st.title("Writer.AI")
st.header("Generate Blog or Article")

# User inputs
content_type = st.selectbox("Select the type of content:", ["Blog", "Article"])
user_input = st.text_input("Enter a topic:", key="user_input")
submit = st.button("Generate")

if submit and user_input:
    # Call your AI model function to generate content based on user input
    response = get_gemini_response(content_type, user_input)
    if response:
        st.subheader(f"Generated {content_type}")
        for chunk in response:
            st.write(chunk.text)
    else:
        st.error("Failed to generate content. Please try again later.")
elif submit and not user_input:
    st.warning("Please enter a topic before submitting.")
