from fastapi import FastAPI
import joblib 
import numpy as np
import pandas as pd
from app.schema import MoodInput
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MoodFuel: Smart coffee Strength Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
model = joblib.load("model/model.pkl")

@app.get("/")
def read_root():
    return {"message": "welcome to MoodFuel API - Predict your perfect coffee strength"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict_strength(data: MoodInput):
    input_data = pd.DataFrame([data.model_dump()])
    prediction = model.predict(input_data)[0]
    return {"recommended_strength": round(float(prediction), 2)}