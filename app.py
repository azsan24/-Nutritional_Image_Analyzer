import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

try:
    genai.configure(api_key=os.getenv("Google_API_KEY"))
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please ensure your 'Google_API_KEY' is correctly set in your .env file.")
    st.stop()

def get_gemini_response(input_prompt, image_parts):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if image_parts:
            response = model.generate_content([input_prompt] + image_parts)
        else:
            response = model.generate_content([input_prompt])
            
        return response.text
    except Exception as e:
        st.error(f"Error generating content with Gemini: {e}")
        return "Could not get a response from Gemini. Please try again."

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

st.set_page_config(page_title="Nutritional Image Analyzer")

st.title("Nutritional Image Analyzer")
st.write("Upload an image of your meal, and I'll act as an expert nutritionist to analyze its calorie content and nutritional breakdown.")

input_prompt = """
As an expert nutritionist, your task is to meticulously analyze the food items present in the image.

**Part 1: Calorie Breakdown**
Identify every distinct food item. For each item, provide a precise estimate of its calorie content. Present this information as a numbered list, strictly adhering to the following format:
1. [Identified Food Item] - [Estimated Calories] calories (e.g., 1. Apple - 95 calories)
2. [Identified Food Item] - [Estimated Calories] calories
...

**Part 2: Health Assessment & Nutritional Breakdown**
After detailing the individual items, provide an overall health assessment of the entire meal. Clearly state whether the food is generally considered 'Healthy' or 'Not Healthy'.

Subsequently, provide an estimated percentage distribution of the key macronutrients and micronutrients for the entire meal. Include:
- **Carbohydrates:** [Percentage]%
- **Fats:** [Percentage]%
- **Proteins:** [Percentage]%
- **Fibers:** [Percentage]%
- **Sugars:** [Percentage]% (if applicable and estimable)
- Mention the Total Calories present and Also mention any other notable vitamins or minerals (e.g., Vitamin C, Iron) if their presence is evident from the food items.

Ensure your response is clear, precise, and directly addresses all parts of this prompt.
"""

uploaded_file = st.file_uploader("Choose an image of your meal...", type=["jpg", "jpeg", "png"])
image_data = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    image_data = input_image_setup(uploaded_file)
else:
    st.info("Please upload an image to get started.")

submit_button = st.button("Analyze My Meal!")

if submit_button:
    if image_data:
        with st.spinner("Analyzing your meal..."):
            response_text = get_gemini_response(input_prompt, image_data)
        
        st.subheader("Nutritional Analysis:")
        st.write(response_text)
    else:
        st.warning("Please upload an image before clicking 'Analyze My Meal!'.")