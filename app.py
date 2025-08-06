import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env variables locally (ignored in deployment)
load_dotenv()

# Configure Gemini API Key from env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ Gemini API key not found. Set GEMINI_API_KEY in your environment.")
    st.stop()

genai.configure(api_key=api_key)

# Meal Plan Generator
def generate_meal_plan(weight, height, goal, ingredients):
    try:
        prompt = f"""
        Act as a professional fitness dietician.
        The user has the following profile:
        - Weight: {weight} kg
        - Height: {height} cm
        - Goal: {goal}

        Available ingredients: {ingredients}

        Create a detailed high-protein meal plan using ONLY the available ingredients.
        Suggest 3–5 meals for the day (breakfast, lunch, dinner, snacks if needed).
        Include approximate protein and carb content per meal.
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ An error occurred while generating your plan:\n\n{str(e)}"

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="NutriMate - AI Fitness Meal Planner", layout="centered")

st.title("🥗 NutriMate")
st.subheader("Your AI Fitness Meal Companion")
st.markdown("Get your personalized high-protein diet plan using AI – based on your body and ingredients you have at home.")

# Input form
with st.form("meal_form"):
    weight = st.number_input("Your Weight (kg)", min_value=30, max_value=200, value=70)
    height = st.number_input("Your Height (cm)", min_value=130, max_value=220, value=175)
    goal = st.radio("Your Fitness Goal", ["Weight Loss", "Muscle Gain", "General Wellness"])
    ingredients = st.text_area("Available Ingredients (comma-separated)", placeholder="e.g., eggs, oats, milk, banana")

    submitted = st.form_submit_button("Generate My Meal Plan 🍽️")

if submitted:
    if not ingredients.strip():
        st.warning("⚠️ Please enter at least one ingredient.")
    else:
        with st.spinner("🤖 Thinking like a nutritionist..."):
            result = generate_meal_plan(weight, height, goal, ingredients)
            st.success("✅ Here's your personalized plan:")
            st.markdown(result)
