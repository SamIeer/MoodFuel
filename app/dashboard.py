# app/streamlit_ui.py
import streamlit as st
import requests
from PIL import Image

# ------------------------------------------------
# 1️⃣ App Config
# ------------------------------------------------
st.set_page_config(
    page_title="MoodFuel ☕ | Coffee Strength Predictor",
    page_icon="☕",
    layout="centered",
)

# ------------------------------------------------
# 2️⃣ Hero Section
# ------------------------------------------------
st.title("☕ MoodFuel — Smart Coffee Strength Recommender")
st.markdown(
    """
    **Feeling sleepy? stressed? or have a long workday ahead?**
    Let **MoodFuel** help you find the *perfect coffee strength* for your day!  
    """
)
# banner = Image.open("https://cdn.pixabay.com/photo/2016/12/27/01/19/coffee-beans-1933047_640.jpg")
# st.image(banner, use_container_width=True)

# ------------------------------------------------
# 3️⃣ Input Section
# ------------------------------------------------
st.subheader("🧠 Enter Your Current Mood Data")

sleep_hours = st.slider("😴 Hours of Sleep", 3.0, 10.0, 7.0, 0.5)
stress_level = st.slider("😤 Stress Level (1–10)", 1, 10, 5)
time_of_day = st.slider("🕒 Time of Day (24h)", 6, 22, 9)
workload_level = st.slider("💻 Workload Level (1–10)", 1, 10, 6)

# ------------------------------------------------
# 4️⃣ Predict Button
# ------------------------------------------------
if st.button("☕ Recommend Coffee Strength"):
    with st.spinner("Calculating your coffee needs..."):
        # Call FastAPI endpoint
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "sleep_hours": sleep_hours,
                    "stress_level": stress_level,
                    "time_of_day": time_of_day,
                    "workload_level": workload_level,
                },
                timeout=10,
            )
            if response.status_code == 200:
                result = response.json()["recommended_strength"]
                st.success(f"✅ Your recommended coffee strength is **{result}/10**!")
                if result > 8:
                    st.image("", caption="You need the strong stuff 💪")
                elif result > 5:
                    st.image("", caption="A balanced cup to keep you going ☕")
                else:
                    st.image("", caption="Just a light brew will do 🌤️")
            else:
                st.error("Error: Could not get response from API.")
        except Exception as e:
            st.error(f"⚠️ API not reachable: {e}")

# ------------------------------------------------
# 5️⃣ Footer
# ------------------------------------------------
st.markdown("---")
st.caption("Built with ❤️ using FastAPI + Streamlit + scikit-learn")
