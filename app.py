## invoice extractor 
from dotenv import load_dotenv

load_dotenv() #load all env variable from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

##lets configure our api key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## FUNCTION TO LOAD GEMINI PRO VISION MODEL AND GET RESPONSE

def get_gemini_response(input,image,prompt):
    #loading the gemini model
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text
def input_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
            'mime_type': uploaded_file.type,
            'data' : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('no file uploaded')
    
##initialise our streamlit app
st.set_page_config(page_title="image invoice extractor")
st.header("gemini application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("choose an image..", type=["jpeg", "jpg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uplaoded Image", use_column_width=True)
    
submit=st.button("tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices, You will have to receive input images as the invoice and later you have to answer query based on input image

"""
##button got clicked

if submit:
    image_data=input_image(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    
    st.subheader("The response is")
    st.write(response)