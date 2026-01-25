from fastapi import FastAPI, Request
import joblib
import pandas as pd
from app.schema import MoodInput
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------
# APP SETUP
# ------------------------------------------------
app = FastAPI(title="MoodFuel: Smart coffee Strength Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# MODEL
# ------------------------------------------------
model = joblib.load("model/model.pkl")




# ------------------------------------------------
# ROUTES
# ------------------------------------------------
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


