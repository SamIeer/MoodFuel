# app/gradio_ui.py
import gradio as gr
import joblib
import pandas as pd
from PIL import Image

# Load model
model = joblib.load("model/model.pkl")

# Define prediction function
def predict_coffee_strength(sleep_hours, stress_level, time_of_day, workload_level):
    data = pd.DataFrame([{
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "time_of_day": time_of_day,
        "workload_level": workload_level,
    }])
    result = model.predict(data)[0]
    return round(float(result), 2)

# Add images for background style
coffee_bg = "app/assets/coffee_banner.jpg"

# Build Gradio UI
demo = gr.Interface(
    fn=predict_coffee_strength,
    inputs=[
        gr.Slider(3, 10, value=7, label="😴 Hours of Sleep"),
        gr.Slider(1, 10, value=5, label="😤 Stress Level"),
        gr.Slider(6, 22, value=9, label="🕒 Time of Day (24h)"),
        gr.Slider(1, 10, value=6, label="💻 Workload Level"),
    ],
    outputs=gr.Number(label="☕ Recommended Coffee Strength (1–10)"),
    title="MoodFuel ☕ — Coffee Strength Predictor",
    description="Find your perfect coffee strength based on sleep, stress, and workload!",
    theme="gradio/soft",
    css="""
        body {
            background: #fdf6f0;
            background-image: url('app/assets/coffee_banner.jpg');
            background-size: cover;
        }
    """,
    examples=[
        [5, 8, 8, 9],
        [7, 3, 11, 4],
        [6, 5, 15, 7]
    ]
)

if __name__ == "__main__":
    demo.launch()
