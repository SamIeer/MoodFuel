# ☕ MoodFuel — AI-Powered Coffee Strength Recommender

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?logo=githubactions)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)
![Gradio](https://img.shields.io/badge/Demo-Gradio-yellow?logo=gradio)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)

> **MoodFuel** is an AI-powered coffee strength recommender that suggests the ideal caffeine intensity based on your mood, stress, and sleep pattern — built using **FastAPI**, **scikit-learn**, **Docker**, and **Streamlit**.  
> It’s a **learning-oriented, open-source project** demonstrating an end-to-end **MLOps pipeline** — from model training to deployment.
> API Endpoint : https://moodfuel-api.onrender.com/
> Streamlit App : https://moodfuel.onrender.com

---

## 🧩 Summary

**MoodFuel** intelligently recommends your coffee strength on a 1–10 scale using data like:
- 😴 Sleep duration
- 😤 Stress level
- 🕒 Time of day
- 💻 Workload intensity  
It demonstrates **machine learning integration with FastAPI**, full **CI/CD automation**, and **modern frontends (Streamlit & Gradio)** for interactivity.

---

## ⚙️ Key Features
- **FastAPI backend** serving ML predictions
- **Streamlit dashboard** for user interaction
- **Gradio demo interface** for ML visualization
- **CI/CD automation** via GitHub Actions
- **Containerized deployment** with Docker
- **Cloud deployment** supported (Render)

---

## 🏗️ Project Architecture
![Architecture](./MoodFuel_Deployment_Architecture.png)

---

## 🗂️ Folder Structure
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

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10
- pip or conda
- Docker 
- GitHub account (for CI/CD setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SamIeer/MoodFuel.git
cd MoodFuel
```
### 2️⃣ Install Dependencies
``` 
pip install -r deploy/requirements.txt
```

### 3️⃣ Train the Model
``` 
python train_model.py
 ```

### 4️⃣ Run FastAPI Backend
```
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs
```
### 💻 Run Frontend Interfaces
Streamlit Dashboard
``` 
streamlit run app/dashboard.py
 ```

Gradio Demo
``` 
python app/gradio_ui.py
```


🐳 Docker Deployment
Build Docker Image
bash
Copy code
```
docker build -t moodfuel-api .
```
Run Container
``` 
docker run -d -p 8000:8000 moodfuel-api 
Access your app at:
```
👉 http://localhost:8000/docs

- ☁️ Cloud Deployment (Render)
- Push your project to GitHub.
- Go to Render
- Create a New Web Service → connect GitHub repo.
- Select Docker environment → deploy.
- Your live AAP will be available at:
- https://moodfuel.onrender.com

CI/CD automatically runs these tests on every push (see .github/workflows/ci.yml).

## 🚀 Contributing

Contributions are welcome! To get started, follow these steps:

1️⃣ Create a New Branch
```
git checkout -b feature/your-feature-name
```

2️⃣ Make Your Changes

✔ Follow PEP 8 style guidelines
✔ Add clear comments and docstrings
✔ Keep your code readable and consistent

3️⃣ Run Tests
```
pytest -v
```

4️⃣ Commit & Push
```
git add .
git commit -m "Add new feature"
git push origin feature/your-feature-name
```

5️⃣ Submit a Pull Request

Open a Pull Request from your branch into the main branch and describe your changes clearly.

## Author

👤 **Sameer Chauhan**

- GitHub: [SamIeer](https://github.com/SamIeer)
- LinkedIn: [Sameer Chauhan](https://www.linkedin.com/in/sameer-chauhan-363298269/)
- Email: **sameerchauhan212204@gmail.com**
