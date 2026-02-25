import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")

st.title("🌍 AI Travel Planner for Students")
st.write("Plan a budget-friendly trip in seconds ✨")

# User inputs
destination = st.text_input("📍 Destination")
days = st.slider("🗓️ Number of days", 1, 14, 3)
budget = st.text_input("💰 Total budget (example: ₹5000)")
interests = st.text_input("🎯 Interests (food, nature, adventure, history)")

if st.button("Generate Itinerary 🚀"):

    if not API_KEY:
        st.error("API key not found. Check your .env file.")
        st.stop()

    if not destination:
        st.warning("Please enter a destination")
        st.stop()

    prompt = f"""
    Create a clear day-by-day travel itinerary.

    Destination: {destination}
    Days: {days}
    Budget: {budget}
    Interests: {interests}

    Include:
    - Daily plan
    - Estimated daily cost
    - Travel tips
    Keep it concise.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    with st.spinner("Planning your trip..."):
        response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        itinerary = result["choices"][0]["message"]["content"]

        st.success("Your trip plan is ready ✅")
        st.markdown(itinerary)

    else:
        st.error("API Error: " + response.text)