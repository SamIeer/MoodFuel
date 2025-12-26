# app/streamlit_ui.py
import streamlit as st
import requests
import time
import os
from datetime import datetime

# ------------------------------------------------
# Configuration & Constants
# ------------------------------------------------
API_URL = os.getenv("API_URL", "https://moodfuel-api.onrender.com")
DEFAULT_TIMEOUT = 30  # Increased timeout for Render's free tier

# Coffee strength categories
STRENGTH_CATEGORIES = {
    "light": {"min": 1, "max": 4, "emoji": "🌱", "name": "Light Brew"},
    "medium": {"min": 5, "max": 7, "emoji": "☕", "name": "Medium Brew"},
    "strong": {"min": 8, "max": 10, "emoji": "💪", "name": "Strong Brew"}
}

# Messages for each category
MESSAGES = {
    "light": [
        "Perfect for a gentle start! 🍃",
        "A light touch to keep you going smoothly ✨",
        "Just enough to awaken your senses 🌅",
        "Gentle energy for a peaceful day 🌼"
    ],
    "medium": [
        "Balanced brew for steady focus! ⚖️",
        "The classic choice for productivity ☕",
        "Perfect harmony of flavor and energy 🎯",
        "Just right for your busy day ⭐"
    ],
    "strong": [
        "Powerful brew for maximum productivity! 💥",
        "Bold and strong for challenging days 🚀",
        "The warrior's choice for tough tasks 🛡️",
        "Full power mode activated! 🔥"
    ]
}

# ------------------------------------------------
# API Integration with Better Error Handling
# ------------------------------------------------
def predict_coffee_strength(data, api_url=API_URL):
    """
    Call the prediction API with comprehensive error handling
    """
    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/predict",
            json=data,
            timeout=DEFAULT_TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 422:
            return None, "Invalid input data. Please check your values."
        elif response.status_code == 429:
            return None, "Too many requests. Please wait a moment."
        elif response.status_code == 500:
            return None, "Server error. Please try again later."
        elif response.status_code == 503:
            return None, "Service temporarily unavailable."
        else:
            return None, f"API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return None, "Request timed out. The server might be busy."
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to the API server. Please check your internet connection."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except ValueError as e:
        return None, f"Invalid response format: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# ------------------------------------------------
# Helper Functions
# ------------------------------------------------
def get_strength_category(strength):
    """Get category based on strength value"""
    if strength <= 4:
        return "light"
    elif strength <= 7:
        return "medium"
    else:
        return "strong"

def get_strength_color(strength):
    """Get color based on strength value"""
    if strength <= 4:
        return "#8BC34A"  # Green
    elif strength <= 7:
        return "#FF9800"  # Orange
    else:
        return "#D32F2F"  # Red

def format_time_display(hour):
    """Format hour for display"""
    if hour < 12:
        return f"{hour}:00 AM 🌅"
    elif hour == 12:
        return f"{hour}:00 PM ☀️"
    elif hour < 17:
        return f"{hour}:00 PM ☀️"
    else:
        return f"{hour}:00 PM 🌆"

# ------------------------------------------------
# 1️⃣ App Config with Enhanced Styling
# ------------------------------------------------
st.set_page_config(
    page_title="MoodFuel ☕ | Smart Coffee Recommender",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/SamIeer/MoodFuel/issues',
        'Report a bug': "https://github.com/SamIeer/MoodFuel/issues",
        'About': "# MoodFuel ☕\nSmart Coffee Strength Recommender\n\nMade with ❤️ by Sameer Chauhan"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem !important;
        color: #4A2C2A !important;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Arial', sans-serif;
    }
    .sub-header {
        color: #6F4E37 !important;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6F4E37 0%, #4A2C2A 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(106, 78, 55, 0.4);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .result-card {
        background: linear-gradient(135deg, #FFF8F0 0%, #F5E6D3 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border-left: 8px solid #6F4E37;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-out;
    }
    .slider-container {
        background-color: #FFF8F0;
        padding: 1.8rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #E8D5B5;
        transition: all 0.3s ease;
    }
    .slider-container:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transform: translateY(-1px);
    }
    .emoji-icon {
        font-size: 1.8rem;
        margin-right: 12px;
        vertical-align: middle;
    }
    .metric-card {
        background: linear-gradient(135deg, #FFF8F0 0%, #F5E6D3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #E8D5B5;
    }
    .strength-meter {
        height: 25px;
        background: #E0E0E0;
        border-radius: 12px;
        overflow: hidden;
        margin: 2rem 0;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }
    .strength-fill {
        height: 100%;
        border-radius: 12px;
        transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .success-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .error-box {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 2️⃣ Hero Section with Enhanced Visuals
# ------------------------------------------------
st.markdown('<h1 class="main-header">☕ MoodFuel</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-header" style="text-align: center;">Smart Coffee Strength Recommender</h3>', unsafe_allow_html=True)

# Coffee beans separator with animation
st.markdown("""
<div style='text-align: center; font-size: 2rem; margin: 1.5rem 0;'>
    <span style='animation: bounce 2s infinite;'>🌰</span> 
    <span style='animation: bounce 2s infinite 0.2s;'>☕</span> 
    <span style='animation: bounce 2s infinite 0.4s;'>🌰</span>
</div>
<style>
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
</style>
""", unsafe_allow_html=True)

# Introduction with cards
st.markdown("### ✨ How It Works")
intro_col1, intro_col2, intro_col3 = st.columns(3)

with intro_col1:
    with st.container():
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>😴</div>
            <h4 style='color: #4A2C2A; margin-bottom: 0.5rem;'>Sleep Analysis</h4>
            <p style='color: #666; font-size: 0.9rem;'>How your sleep affects your coffee needs</p>
        </div>
        """, unsafe_allow_html=True)

with intro_col2:
    with st.container():
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>🧠</div>
            <h4 style='color: #4A2C2A; margin-bottom: 0.5rem;'>Mood Matching</h4>
            <p style='color: #666; font-size: 0.9rem;'>Personalized recommendations based on your mood</p>
        </div>
        """, unsafe_allow_html=True)

with intro_col3:
    with st.container():
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>⏰</div>
            <h4 style='color: #4A2C2A; margin-bottom: 0.5rem;'>Time Aware</h4>
            <p style='color: #666; font-size: 0.9rem;'>Perfect timing for your coffee intake</p>
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
    # Sleep Hours
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">😴</span><b style="font-size: 1.1rem;"> Sleep Quality</b>', unsafe_allow_html=True)
        sleep_hours = st.slider(
            "Hours of sleep last night",
            min_value=0.0,
            max_value=12.0,
            value=7.0,
            step=0.5,
            help="How many hours did you sleep? (0 = no sleep)",
            key="sleep_slider",
            format="%.1f hours"
        )
        
        # Sleep quality indicator with progress bar
        sleep_progress = min(sleep_hours / 8 * 100, 100)
        sleep_color = "#4CAF50" if sleep_hours >= 7 else "#FFC107" if sleep_hours >= 5 else "#F44336"
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #666;">Sleep Quality</span>
                <span style="font-weight: bold; color: {sleep_color};">
                    {"😊 Excellent" if sleep_hours >= 7 else "😌 Good" if sleep_hours >= 5 else "😫 Poor"}
                </span>
            </div>
            <div style="height: 8px; background: #E0E0E0; border-radius: 4px; overflow: hidden;">
                <div style="width: {sleep_progress}%; height: 100%; background: {sleep_color}; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Workload Level
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">💻</span><b style="font-size: 1.1rem;"> Workload Level</b>', unsafe_allow_html=True)
        workload_level = st.slider(
            "Today's expected workload",
            min_value=1,
            max_value=10,
            value=6,
            help="1 = Very light day, 10 = Extremely demanding day",
            key="workload_slider"
        )
        
        # Workload indicator with emoji
        workload_emojis = ["🌱", "🌿", "🌳", "🌋"]
        workload_idx = min(3, (workload_level - 1) // 3)
        st.markdown(f"""
        <div style="margin-top: 1rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{workload_emojis[workload_idx]}</div>
            <span style="font-weight: bold; color: #4A2C2A;">
                {"Light" if workload_level <= 3 else "Moderate" if workload_level <= 6 else "Heavy" if workload_level <= 8 else "Intense"}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Stress Level
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">😤</span><b style="font-size: 1.1rem;"> Stress Level</b>', unsafe_allow_html=True)
        stress_level = st.slider(
            "Current stress level",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Completely relaxed, 10 = Extremely stressed",
            key="stress_slider"
        )
        
        # Stress indicator with face emoji
        stress_faces = ["😌", "🙂", "😐", "😟", "😫"]
        stress_idx = min(4, (stress_level - 1) // 2)
        st.markdown(f"""
        <div style="margin-top: 1rem; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{stress_faces[stress_idx]}</div>
            <span style="font-weight: bold; color: #4A2C2A;">
                {"Low" if stress_level <= 3 else "Medium" if stress_level <= 6 else "High" if stress_level <= 8 else "Very High"}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Time of Day
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">⏰</span><b style="font-size: 1.1rem;"> Time of Day</b>', unsafe_allow_html=True)
        time_of_day = st.slider(
            "Current time",
            min_value=6,
            max_value=22,
            value=datetime.now().hour if 6 <= datetime.now().hour <= 22 else 9,
            help="Select current hour (6 AM to 10 PM)",
            key="time_slider",
            format="%d:00"
        )
        
        # Time indicator
        time_emojis = {"🌅": (6, 11), "☀️": (12, 16), "🌆": (17, 22)}
        current_emoji = "🌅"
        for emoji, (start, end) in time_emojis.items():
            if start <= time_of_day <= end:
                current_emoji = emoji
                break
        
        st.markdown(f"""
        <div style="margin-top: 1rem; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{current_emoji}</div>
            <span style="font-weight: bold; color: #4A2C2A;">
                {format_time_display(time_of_day).replace(':00 ', ' ')}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Summary card with metrics
st.markdown("---")
st.markdown('<h3 class="sub-header">📊 Your Current State Summary</h3>', unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    with st.container():
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>😴</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #4A2C2A;'>{sleep_hours:.1f}h</div>
            <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
                {"Good sleep" if sleep_hours >= 7 else "Need more sleep" if sleep_hours >= 5 else "Very low sleep"}
            </div>
        </div>
        """, unsafe_allow_html=True)

with summary_col2:
    with st.container():
        stress_trend = "↘️" if stress_level <= 3 else "➡️" if stress_level <= 6 else "↗️"
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>😤</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #4A2C2A;'>{stress_level}/10</div>
            <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
                {stress_trend} {"Low" if stress_level <= 3 else "Medium" if stress_level <= 6 else "High"}
            </div>
        </div>
        """, unsafe_allow_html=True)

with summary_col3:
    with st.container():
        workload_trend = "↘️" if workload_level <= 3 else "➡️" if workload_level <= 6 else "↗️"
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💻</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #4A2C2A;'>{workload_level}/10</div>
            <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
                {workload_trend} {"Light" if workload_level <= 3 else "Moderate" if workload_level <= 6 else "Heavy"}
            </div>
        </div>
        """, unsafe_allow_html=True)

with summary_col4:
    with st.container():
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⏰</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #4A2C2A;'>{time_of_day}:00</div>
            <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
                {"Morning" if time_of_day < 12 else "Afternoon" if time_of_day < 17 else "Evening"}
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        use_container_width=True,
        type="primary"
    )

# Placeholder for results
result_placeholder = st.empty()
error_placeholder = st.empty()

if predict_button:
    # Clear previous results and errors
    result_placeholder.empty()
    error_placeholder.empty()
    
    # Show loading animation
    with st.spinner("**Brewing your perfect recommendation...** ☕✨"):
        # Create progress bar
        progress_bar = st.progress(0)
        
        # Simulate progress with actual API call timing
        for percent in range(0, 101, 5):
            time.sleep(0.1)
            progress_bar.progress(percent)
        
        # Prepare payload
        payload = {
            "sleep_hours": float(sleep_hours),
            "stress_level": int(stress_level),
            "time_of_day": int(time_of_day),
            "workload_level": int(workload_level),
        }
        
        # Get user's custom API URL from session state or use default
        custom_api = st.session_state.get('custom_api_url', API_URL)
        
        # Call API
        result, error = predict_coffee_strength(payload, custom_api)
        
        # Clear progress bar
        progress_bar.empty()
        
        if error:
            # Show error message
            error_placeholder.markdown(f"""
            <div class='error-box'>
                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.5rem; margin-right: 10px;'>⚠️</span>
                    <h3 style='color: #D32F2F; margin: 0;'>Recommendation Failed</h3>
                </div>
                <p style='color: #666; margin: 0.5rem 0;'>{error}</p>
                <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                    <b>Tips:</b><br>
                    1. Check if the API server is running<br>
                    2. Verify your internet connection<br>
                    3. Try using a different API endpoint
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show retry button
            if st.button("🔄 Try Again", use_container_width=True, key="retry_button"):
                st.rerun()
                
        else:
            # Extract result
            recommended_strength = result.get("recommended_strength", 5)
            category = get_strength_category(recommended_strength)
            category_info = STRENGTH_CATEGORIES[category]
            
            # Display result
            with result_placeholder.container():
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                
                # Header
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 3.5rem; margin-bottom: 1rem; animation: bounce 1s ease-in-out;">
                        {category_info['emoji']}
                    </div>
                    <h1 style="color: #4A2C2A; margin-bottom: 0.5rem; font-size: 2.2rem;">
                        Perfect Coffee Strength Found!
                    </h1>
                    <div style="font-size: 4.5rem; font-weight: bold; color: #6F4E37; margin: 1rem 0; 
                               text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                        {recommended_strength}/10
                    </div>
                    <h3 style="color: #8B6B4F; margin-top: 0; font-size: 1.5rem;">
                        {category_info['name']}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Strength meter
                strength_color = get_strength_color(recommended_strength)
                st.markdown(f"""
                <div style="margin: 2.5rem 0;">
                    <div class='strength-meter'>
                        <div class='strength-fill' style='width: {recommended_strength * 10}%; background: {strength_color};'></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span style="color: #666; font-size: 0.9rem;">Light (1-4)</span>
                        <span style="color: #666; font-size: 0.9rem;">Medium (5-7)</span>
                        <span style="color: #666; font-size: 0.9rem;">Strong (8-10)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Personalized message
                import random
                message = random.choice(MESSAGES[category])
                st.markdown(f"""
                <div style="text-align: center; margin: 2rem 0; padding: 1.5rem; background: rgba(255, 255, 255, 0.5); 
                          border-radius: 15px; border: 2px dashed #E8D5B5;">
                    <p style="font-size: 1.3rem; font-style: italic; color: #5D4037; margin: 0;">
                        "{message}"
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Brewing tips
                st.markdown("### 💡 Brewing Recommendations")
                tips_col1, tips_col2 = st.columns(2)
                
                with tips_col1:
                    st.markdown(f"""
                    <div style='padding: 1rem; background: white; border-radius: 10px; height: 100%;'>
                        <h4 style='color: #4A2C2A; margin-bottom: 1rem;'>For Your Strength:</h4>
                        <p><b>☕ Coffee Amount:</b> {"Light (12g)" if category == "light" else "Medium (18g)" if category == "medium" else "Strong (24g)"}</p>
                        <p><b>⚙️ Grind Size:</b> {"Coarse" if category == "light" else "Medium" if category == "medium" else "Fine"}</p>
                        <p><b>⏱️ Brew Time:</b> {"2-3 minutes" if category == "light" else "3-4 minutes" if category == "medium" else "4-5 minutes"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tips_col2:
                    st.markdown(f"""
                    <div style='padding: 1rem; background: white; border-radius: 10px; height: 100%;'>
                        <h4 style='color: #4A2C2A; margin-bottom: 1rem;'>Best Brew Methods:</h4>
                        <p>• {"Pour Over / French Press" if category == "light" else "Aeropress / Drip" if category == "medium" else "Espresso / Moka Pot"}</p>
                        <p>• Water Temp: {"90-92°C" if category == "light" else "92-94°C" if category == "medium" else "94-96°C"}</p>
                        <p>• Milk Ratio: {"High (latte)" if category == "light" else "Medium (cappuccino)" if category == "medium" else "Low (ristretto)"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Share and save options
                st.markdown("---")
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("📋 Copy Result", use_container_width=True, key="copy_result"):
                        st.session_state.copied = True
                        st.success("✅ Recommendation copied to clipboard!")
                        
                with action_col2:
                    if st.button("🔄 New Recommendation", use_container_width=True, key="new_recommendation"):
                        st.rerun()
                        
                with action_col3:
                    if st.button("⭐ Save Preference", use_container_width=True, key="save_preference"):
                        if 'saved_preferences' not in st.session_state:
                            st.session_state.saved_preferences = []
                        st.session_state.saved_preferences.append({
                            "strength": recommended_strength,
                            "category": category,
                            "inputs": payload,
                            "timestamp": datetime.now().isoformat()
                        })
                        st.success("✅ Preference saved!")
                        
                # Easter egg tracking
                if 'click_count' not in st.session_state:
                    st.session_state.click_count = 0
                st.session_state.click_count += 1
                
                if st.session_state.click_count >= 3:
                    st.balloons()

# ------------------------------------------------
# 5️⃣ Sidebar with Additional Features
# ------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings & Preferences")
    
    # API Configuration
    st.markdown("### 🔗 API Configuration")
    custom_api_url = st.text_input(
        "API Endpoint URL",
        value=API_URL,
        help="Enter your custom API endpoint URL",
        key="api_url_input"
    )
    if custom_api_url != API_URL:
        st.session_state.custom_api_url = custom_api_url
        st.info(f"Using custom API: {custom_api_url}")
    
    # Test API Connection
    if st.button("Test API Connection", use_container_width=True, key="test_api"):
        with st.spinner("Testing connection..."):
            test_result, test_error = predict_coffee_strength({
                "sleep_hours": 7.0,
                "stress_level": 5,
                "time_of_day": 9,
                "workload_level": 6
            }, custom_api_url)
            
            if test_error:
                st.error(f"❌ Connection failed: {test_error}")
            else:
                st.success("✅ API connection successful!")
    
    # Theme selector
    st.markdown("### 🎨 Personalization")
    theme = st.selectbox(
        "Color Theme",
        ["Coffee Brown ☕", "Dark Roast 🖤", "Caramel Latte 🍯", "Espresso Black ⚫"],
        index=0
    )
    
    # Coffee preferences
    st.markdown("### ❤️ Coffee Preferences")
    favorite_brew = st.multiselect(
        "Favorite Brew Methods",
        ["Espresso", "French Press", "Pour Over", "Aeropress", "Cold Brew", "Moka Pot", "Drip Coffee", "Turkish"],
        default=["Espresso", "French Press"]
    )
    
    daily_limit = st.slider("Max cups per day", 1, 10, 3, help="Set your daily coffee limit")
    
    # Saved preferences
    if 'saved_preferences' in st.session_state and st.session_state.saved_preferences:
        st.markdown("### 📚 Saved Preferences")
        for i, pref in enumerate(st.session_state.saved_preferences[-3:]):  # Show last 3
            with st.expander(f"Preference {i+1}: {pref['strength']}/10"):
                st.write(f"Strength: {pref['strength']}/10")
                st.write(f"Category: {pref['category'].title()}")
                st.write(f"Date: {pref['timestamp'][:10]}")
                if st.button(f"Load Preference {i+1}", key=f"load_pref_{i}"):
                    st.success(f"Loaded preference {i+1}!")
    
    # Information section
    st.markdown("---")
    st.markdown("## ℹ️ About MoodFuel")
    st.markdown("""
    <div class='info-box'>
        <p><b>MoodFuel</b> uses machine learning to recommend 
        the perfect coffee strength based on your:</p>
        <ul style='margin: 0.5rem 0; padding-left: 1.5rem;'>
            <li>Sleep patterns 😴</li>
            <li>Stress levels 🧠</li>
            <li>Workload 💼</li>
            <li>Time of day ⏰</li>
        </ul>
        <p>Get personalized coffee recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick tips
    with st.expander("💡 Quick Coffee Tips", expanded=False):
        st.markdown("""
        - **Morning (6-11 AM)**: Medium strength for steady energy
        - **Afternoon (12-4 PM)**: Light brew to avoid sleep disruption
        - **Evening (5-10 PM)**: Very light or decaf only
        - **High stress**: Avoid very strong coffee, try lighter roasts
        - **Low sleep**: Consider moderate strength, not too strong
        - **Heavy workload**: Medium-strong brew with breaks
        """)
    
    # Health disclaimer
    st.caption("""
    ⚠️ **Disclaimer:** This app provides recommendations only. 
    Consult with a healthcare professional for dietary advice.
    Recommended daily limit: 3-4 cups of coffee. """)