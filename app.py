import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
import pandas as pd

# Configure the api_key
genai.configure(api_key = os.getenv('Google_API_Key'))

# Streamlit Page Styling
st.set_page_config(page_title="Healthcare Advisor", page_icon="⚕️", layout="wide")

# Custom CSS for extra styling
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        color: #1f77b4;
    }
    .bmi-box {
        background-color: #f0f9f9;
        padding: 15px;
        border-radius: 10px;
    }
    .bmi-status {
        padding: 5px 10px;
        border-radius: 8px;
        color: white;
        display: inline-block;
    }
    .underweight { background: #ff9800; }
    .normal { background: #4caf50; }
    .overweight { background: #ff5722; }
    .obese { background: #f44336; }
    </style>
""", unsafe_allow_html=True)

# Header
st.header("👨‍⚕️ Healthcare :blue[Advisor] ⚕️", divider="green")
st.markdown("#### 🤖 *Your AI-powered assistant for health, fitness & wellness!*")

# Layout: Split page into 2 columns
col1, col2 = st.columns([2, 1])

with col1:
    input = st.text_input('💬 **Ask me about health, diseases or fitness tips:**', placeholder="e.g., How can I boost my immune system?")
    submit = st.button("🔍 Get Advice")

    if submit and input:
        with st.spinner("Generating response..."):
            def get_response(text_input):
                model = genai.GenerativeModel("gemini-1.5-pro")
                myprompt = '''I want you to act as a Dietician and Healthcare Expert
                and answer questions related to Health, Diseases & Fitness only. If asked about medications, reply with:
                "Please reach out to your Doctor for Medication." Non-health topics should be declined politely. Here's the question: '''
                response = model.generate_content(myprompt + text_input)
                return response.text

            response = get_response(input)
            st.success("🩺 Here's my advice:")
            st.markdown(response)

with col2:
    st.subheader("🧮 BMI Calculator")
    with st.form("bmi_form"):
        weight = st.text_input("⚖️ Weight (in kgs)", placeholder="e.g., 70")
        height = st.text_input("📏 Height (in cms)", placeholder="e.g., 175")
        calc_btn = st.form_submit_button("📊 Calculate BMI")

    if calc_btn and weight and height:
        weight = pd.to_numeric(weight, errors="coerce")
        height = pd.to_numeric(height, errors="coerce")
        if pd.notnull(weight) and pd.notnull(height) and height > 0:
            height_mts = height / 100
            bmi = round(weight / (height_mts ** 2), 2)

            # Interpret BMI
            if bmi < 18.5:
                status = "Underweight"
                css_class = "underweight"
            elif 18.5 <= bmi < 25:
                status = "Normal"
                css_class = "normal"
            elif 25 <= bmi < 30:
                status = "Overweight"
                css_class = "overweight"
            else:
                status = "Obese"
                css_class = "obese"

            st.markdown(f"""
                <div class="bmi-box">
                    <p class="big-font">Your BMI is: <strong>{bmi}</strong></p>
                    <p>Status: <span class="bmi-status {css_class}">{status}</span></p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                **Interpretation Guide:**  
                - *Underweight:* BMI < 18.5  
                - *Normal:* BMI 18.5 - 24.9  
                - *Overweight:* BMI 25 - 29.9  
                - *Obese:* BMI ≥ 30
            """)

# Divider & Disclaimer
st.markdown("---")
st.subheader("⚠️ Disclaimer")
st.info('''
1. This AI tool is for educational and advisory purposes only.
2. Always consult a licensed medical professional before making health decisions.
''')
