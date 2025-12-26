# app/streamlit_ui.py
import streamlit as st
import requests
from PIL import Image
import base64
from io import BytesIO
import time
import os 
import requests

# ------------------------------------------------
# API integration
# ------------------------------------------------
API_URL = os.getenv("API_URL", "https://moodfuel-api.onrender.com")

def predict(data):
    res = requests.post(f"{API_URL}/predict", json=data, timeout=15)
    res.raise_for_status()
    return res.json()


# ------------------------------------------------
# 1️⃣ App Config with Enhanced Styling
# ------------------------------------------------
st.set_page_config(
    page_title="MoodFuel ☕ | Smart Coffee Recommender",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem !important;
        color: #4A2C2A !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #6F4E37 !important;
        font-weight: 400;
    }
    .stButton button {
        background: linear-gradient(135deg, #6F4E37 0%, #4A2C2A 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(106, 78, 55, 0.3);
    }
    .result-card {
        background: linear-gradient(135deg, #FFF8F0 0%, #F5E6D3 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #6F4E37;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .slider-container {
        background-color: #FFF8F0;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .emoji-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 2️⃣ Hero Section with Enhanced Visuals
# ------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<h1 class="main-header">☕ MoodFuel</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="sub-header" style="text-align: center;">Smart Coffee Strength Recommender</h3>', unsafe_allow_html=True)
    
    # Coffee beans separator
    st.markdown("<div style='text-align: center; font-size: 2rem; margin: 1rem 0;'>🌰 • ☕ • 🌰</div>", unsafe_allow_html=True)

# Introduction with cards
intro_col1, intro_col2, intro_col3 = st.columns(3)

with intro_col1:
    with st.container():
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>😴</div>
            <h4>Sleep Analysis</h4>
            <p>How your sleep affects your coffee needs</p>
        </div>
        """, unsafe_allow_html=True)

with intro_col2:
    with st.container():
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>🧠</div>
            <h4>Mood Matching</h4>
            <p>Personalized recommendations</p>
        </div>
        """, unsafe_allow_html=True)

with intro_col3:
    with st.container():
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>⏰</div>
            <h4>Time Aware</h4>
            <p>Perfect timing for your coffee</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------
# 3️⃣ Input Section with Better Organization
# ------------------------------------------------
st.markdown('<h2 class="sub-header">🎯 Tell Us About Your Day</h2>', unsafe_allow_html=True)
st.markdown("*Adjust the sliders below to reflect your current state*")

# Create two columns for better layout
col_left, col_right = st.columns(2)

with col_left:
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">😴</span><b> Sleep Quality</b>', unsafe_allow_html=True)
        sleep_hours = st.slider(
            "Hours of sleep last night",
            min_value=3.0,
            max_value=12.0,
            value=7.0,
            step=0.5,
            help="How many hours did you sleep?",
            key="sleep_slider"
        )
        
        # Sleep quality indicator
        sleep_quality = "😊 Excellent" if sleep_hours >= 7.5 else "😌 Good" if sleep_hours >= 6 else "😐 Fair" if sleep_hours >= 5 else "😫 Poor"
        st.caption(f"Sleep Quality: {sleep_quality} ({sleep_hours} hours)")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">💻</span><b> Workload Level</b>', unsafe_allow_html=True)
        workload_level = st.slider(
            "Today's expected workload",
            min_value=1,
            max_value=10,
            value=6,
            help="1 = Light day, 10 = Very demanding day",
            key="workload_slider"
        )
        
        # Workload indicator
        workload_desc = ["🌱 Light", "🌿 Moderate", "🌳 Heavy", "🌋 Intense"]
        workload_idx = min(3, (workload_level - 1) // 3)
        st.caption(f"Workload: {workload_desc[workload_idx]}")
        
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">😤</span><b> Stress Level</b>', unsafe_allow_html=True)
        stress_level = st.slider(
            "Current stress level",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very relaxed, 10 = Highly stressed",
            key="stress_slider"
        )
        
        # Stress indicator with color bar
        stress_color = "#4CAF50" if stress_level <= 3 else "#FFC107" if stress_level <= 6 else "#F44336"
        st.markdown(f'<div style="height: 8px; background: linear-gradient(to right, #4CAF50, #FFC107, #F44336); border-radius: 4px;"><div style="width: {stress_level*10}%; height: 100%; background-color: {stress_color}; border-radius: 4px;"></div></div>', unsafe_allow_html=True)
        st.caption(f"Stress Level: {stress_level}/10")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">⏰</span><b> Time of Day</b>', unsafe_allow_html=True)
        time_of_day = st.slider(
            "Current time (24-hour format)",
            min_value=6,
            max_value=22,
            value=9,
            help="Early morning to evening",
            key="time_slider"
        )
        
        # Time of day indicator
        time_period = "🌅 Morning" if time_of_day < 12 else "☀️ Afternoon" if time_of_day < 17 else "🌆 Evening"
        st.caption(f"{time_period} ({time_of_day}:00)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Summary card
st.markdown("---")
st.markdown('<h3 class="sub-header">📊 Your Current State Summary</h3>', unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.metric("Sleep Hours", f"{sleep_hours}h", 
              f"{'+Good' if sleep_hours >= 7 else '-Need more' if sleep_hours >= 5 else '--Low'}")

with summary_col2:
    st.metric("Stress Level", f"{stress_level}/10",
              f"{'Low' if stress_level <= 3 else 'Medium' if stress_level <= 6 else 'High'}")

with summary_col3:
    st.metric("Workload", f"{workload_level}/10",
              f"{'Light' if workload_level <= 3 else 'Moderate' if workload_level <= 6 else 'Heavy'}")

with summary_col4:
    st.metric("Time", f"{time_of_day}:00",
              f"{'Morning' if time_of_day < 12 else 'Afternoon' if time_of_day < 17 else 'Evening'}")

# ------------------------------------------------
# 4️⃣ Predict Button with Enhanced Feedback
# ------------------------------------------------
st.markdown("---")
st.markdown('<h2 class="sub-header">☕ Get Your Coffee Recommendation</h2>', unsafe_allow_html=True)

# Center the button
button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    predict_button = st.button(
        "🚀 **Recommend My Perfect Coffee Strength** 🚀",
        use_container_width=True
    )

# Placeholder for results
result_placeholder = st.empty()

if predict_button:
    with st.spinner("**Brewing your perfect recommendation...** ☕✨"):
        # Add a progress bar for better UX
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        # Call FastAPI endpoint
        payload = {
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "time_of_day": time_of_day,
            "workload_level": workload_level,
        }
        try:
            response = predict(payload)

            result = response["recommended_strength"]
            
            if response.status_code == 200:
                result = response.json()["recommended_strength"]
                
                # Clear progress bar
                progress_bar.empty()
                
                # Display result with enhanced styling
                with result_placeholder.container():
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    # Coffee strength meter
                    strength_emoji = "🌱" if result <= 4 else "☕" if result <= 7 else "💪"
                    strength_text = "Light Brew" if result <= 4 else "Medium Brew" if result <= 7 else "Strong Brew"
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{strength_emoji}</div>
                        <h1 style="color: #4A2C2A; margin-bottom: 0.5rem;">Your Recommended Strength</h1>
                        <div style="font-size: 4rem; font-weight: bold; color: #6F4E37; margin: 1rem 0;">{result}/10</div>
                        <h3 style="color: #8B6B4F; margin-top: 0;">{strength_text}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Visual strength indicator
                    strength_width = result * 10
                    strength_color = "#8BC34A" if result <= 4 else "#FF9800" if result <= 7 else "#D32F2F"
                    st.markdown(f"""
                    <div style="background: #E0E0E0; height: 20px; border-radius: 10px; margin: 2rem 0;">
                        <div style="width: {strength_width}%; height: 100%; background: {strength_color}; border-radius: 10px; transition: width 1s ease;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Personalized message
                    messages = {
                        "light": [
                            "Perfect for a gentle start! 🍃",
                            "A light touch to keep you going smoothly ✨",
                            "Just enough to awaken your senses 🌅"
                        ],
                        "medium": [
                            "Balanced brew for steady focus! ⚖️",
                            "The classic choice for productivity ☕",
                            "Perfect harmony of flavor and energy 🎯"
                        ],
                        "strong": [
                            "Powerful brew for maximum productivity! 💥",
                            "Bold and strong for challenging days 🚀",
                            "The warrior's choice for tough tasks 🛡️"
                        ]
                    }
                    
                    category = "light" if result <= 4 else "medium" if result <= 7 else "strong"
                    import random
                    message = random.choice(messages[category])
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; background: rgba(255, 255, 255, 0.7); border-radius: 10px;">
                        <p style="font-size: 1.2rem; font-style: italic; color: #5D4037;">"{message}"</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Brewing tips based on strength
                    st.markdown("### 💡 Brewing Tips")
                    tips_col1, tips_col2 = st.columns(2)
                    
                    with tips_col1:
                        st.markdown("""
                        **Grind Size:**
                        - Light: Coarse grind
                        - Medium: Medium grind  
                        - Strong: Fine grind
                        """)
                    
                    with tips_col2:
                        st.markdown("""
                        **Brew Time:**
                        - Light: 2-3 minutes
                        - Medium: 3-4 minutes
                        - Strong: 4-5 minutes
                        """)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Share button
                    st.markdown("---")
                    share_col1, share_col2, share_col3 = st.columns([1, 2, 1])
                    with share_col2:
                        if st.button("📋 Copy Recommendation", use_container_width=True):
                            st.session_state.copied = True
                            st.rerun()
                    
                    if 'copied' in st.session_state and st.session_state.copied:
                        st.success("✅ Recommendation copied to clipboard!")
                        st.session_state.copied = False
                        
            else:
                st.error("⚠️ Could not get a recommendation. Please try again.")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 **API Connection Error**")
            st.info("Please make sure the FastAPI server is running on http://127.0.0.1:8000")
            st.code("uvicorn app.main:app --reload", language="bash")
            
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")

# ------------------------------------------------
# 5️⃣ Sidebar with Additional Features
# ------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # API Configuration
    st.markdown("### 🔗 API Settings")
    api_url = st.text_input(
        "API Endpoint",
        value=API_URL,
        help="Change if your API is hosted elsewhere"
    )
    # API_URL = custom_api
    
    # Theme selector
    st.markdown("### 🎨 Theme")
    theme = st.selectbox(
        "Choose color theme",
        ["Coffee Brown", "Dark Roast", "Caramel Latte"],
        index=0
    )
    
    # Coffee preferences
    st.markdown("### ❤️ Your Preferences")
    favorite_brew = st.multiselect(
        "Favorite brewing methods",
        ["Espresso", "French Press", "Pour Over", "Aeropress", "Cold Brew", "Moka Pot"]
    )
    
    daily_limit = st.slider("Max cups per day", 1, 8, 3)
    
    # Information section
    st.markdown("---")
    st.markdown("## ℹ️ About MoodFuel")
    st.info("""
    **MoodFuel** uses machine learning to recommend 
    the perfect coffee strength based on your:
    - Sleep patterns 😴
    - Stress levels 🧠
    - Workload 💼
    - Time of day ⏰
    
    Get personalized coffee recommendations!
    """)
    
    # Quick tips
    with st.expander("💡 Quick Coffee Tips"):
        st.markdown("""
        - **Morning**: Medium strength for steady energy
        - **Afternoon**: Light brew to avoid sleep disruption
        - **Stressed**: Avoid very strong coffee
        - **Low sleep**: Consider moderate strength
        """)

# ------------------------------------------------
# 6️⃣ Footer with Enhanced Information
# ------------------------------------------------
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("### 🛠️ Built With")
    st.markdown("""
    - Python 🐍
    - FastAPI ⚡
    - Streamlit 🎈
    - scikit-learn 🤖
    """)

with footer_col2:
    st.markdown("### 📚 Learn More")
    st.markdown("""
    [GitHub Repository](https://github.com/SamIeer/MoodFuel)  
    [Documentation](https://github.com/SamIeer/MoodFuel/blob/main/README.md)  
    [Coffee Science](https://example.com)
    """)

with footer_col3:
    st.markdown("### 📞 Support")
    st.markdown("""
    Found a bug? [Report here](https://github.com/SamIeer/MoodFuel/issues)  
    """)
# Want a feature? [Request here](https://github.com/discussions)  
#     Questions? [Join our community](https://discord.gg/example)
st.markdown("---")
st.caption("""
<div style="text-align: center; color: #666;">
    Made with ❤️ and lots of ☕ by Sameer Chauhan• 
    <i>Enjoy your perfect brew!</i> • 
    v1.0.0 © 2025
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 7️⃣ Easter Egg / Fun Feature
# ------------------------------------------------
if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

if predict_button:
    st.session_state.click_count += 1
    
if st.session_state.click_count >= 5:
    st.balloons()
    st.sidebar.success("🎉 You're a coffee connoisseur! Unlocked: Master Brewer mode!")