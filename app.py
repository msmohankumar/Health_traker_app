import streamlit as st
from dotenv import load_dotenv
load_dotenv() # Activate the Local Vars...
#from langchain_google_genai import PromptTemplate, LLMChain
import google.generativeai as genai
import os
import pandas as pd

# Configure the api_key
genai.configure(api_key = os.getenv('Google_API_Key'))

# Streamlit Page
st.header("👨‍⚕️ Healthcare :blue[Advisor] ⚕️", divider = "green")
input = st.text_input('''Hi! I am your medical expert 💊.
                      Ask me information about Health, Diseases & Fitness Only''')

submit = st.button("Submit")

# BMI Calculator
st.sidebar.subheader("BMI Calculator ✍️")
weight = st.sidebar.text_input("Weight (in kgs): ")
height = st.sidebar.text_input("Height (in cms): ")

# Calculate the BMI
weight = pd.to_numeric(weight)
height = pd.to_numeric(height)
height_mts = height/100
bmi = weight/(height_mts**2)

# Scale of the BMI
notes = f'''The BMI value can be interpreted as:
* Underweight: BMI<18.5
* Normal Weight: BMI 18.5 - 24.9
* Overweight: BMI 25 - 29.9
* Obese: BMI > 30'''

if bmi:
    st.sidebar.markdown("The BMI is: ")
    st.sidebar.write(bmi)
    st.sidebar.write(notes)

# Generative AI Application
def get_response(text_input):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if text_input!="":
        myprompt = '''I want you to acts as a Dietician and Healthcare Expert
and answer the questions on Health & Related Topics Only. If the User is asking information/
prompting on the topics other than Health, just pass the Message - "I am a Healthcare Chatbot
and can answer questions related to Health , Diseases & Fitness Only". Please note if someone asks for
medicines or medicines name, just pass the message -  "Please reach out to your Doctor for Medication."
So, here is the Question...'''
        response = model.generate_content(myprompt+text_input)
        return(response.text)
    else:
        st.write("Please Enter the Prompt!!")
        
if submit:
    response = get_response(input)
    st.subheader("The :orange[Response] is: ")
    st.write(response)
    
# Disclaimer
st.subheader("Disclaimer: ", divider = True)
notes = f'''
1. This is an AI Advisor and should not be construed as a Medical Advise.
2. Before taking any action, it is recommended to consult a Medical Practitioner.'''

st.markdown(notes)
