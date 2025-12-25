# ☕ MoodFuel — Smart Coffee Strength Recommender

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-black?logo=githubactions)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange?logo=scikitlearn)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)
![Gradio](https://img.shields.io/badge/Demo-Gradio-yellow?logo=gradio)

> **MoodFuel** is an intelligent FastAPI + ML web app that predicts your **ideal coffee strength** based on your mood, stress, and sleep pattern — built with full MLOps workflow (Model + API + CI/CD + Docker + UI + Deployment).

---

## 🚀 Project Overview

### 🌟 Why MoodFuel?
Everyone drinks coffee — but how much strength do you *actually* need?  
MoodFuel helps you find the **perfect coffee intensity (1–10)** based on:
- 😴 Hours of sleep  
- 😤 Stress level  
- 💻 Workload intensity  
- 🕒 Time of day  

Trained using `RandomForestRegressor`, the app recommends a caffeine level that balances focus and energy.

---

## 🧠 Tech Stack

| Layer | Tool |
|:--|:--|
| **ML Model** | scikit-learn, pandas, numpy |
| **API Framework** | FastAPI |
| **Containerization** | Docker |
| **Continuous Integration** | GitHub Actions |
| **Frontend UIs** | Streamlit, Gradio |
| **Deployment** | Render, Hugging Face Spaces, AWS ECS |

---

## 🏗️ Architecture Diagram

![MoodFuel Deployment Architecture](./MoodFuel_Deployment_Architecture.png)

**Pipeline Overview:**
1. Synthetic data generated with `DataGenerator.py`
2. Model trained using `train_model.py` → saved as `model.pkl`
3. FastAPI serves `/predict` endpoint
4. Streamlit and Gradio provide interactive UIs
5. Docker + CI/CD enable reproducible, automated deployment

---

## 🗂️ Project Structure

```
├── .gitignore
├── app
    ├── __init__.py
    ├── __pycache__
    │   ├── main.cpython-312.pyc
    │   ├── schema.cpython-312.pyc
    │   └── __init__.cpython-312.pyc
    ├── schema.py
    ├── main.py
    ├── gradio_ui.py
    └── dashboard.py
├── model
    └── model.pkl
├── requirements.txt
├── deploy
    └── .dockerignore
├── tests
    └── test_app.py
├── Dockerfile
├── data
    ├── DataGenerator.py
    └── coffee_strength_dataset.csv
├── .github
    └── workflows
    │   └── ci.yml
└── train_model.py
```
