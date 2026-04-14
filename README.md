# 🧠 Cognitive Pattern Analyzer

A machine learning-powered web application that detects cognitive distortions in user input text.

---

## 🚀 Features

* Detects cognitive distortions (e.g., catastrophizing, overgeneralization)
* REST API built with FastAPI
* Interactive UI built with Streamlit
* ML model using sentence embeddings

---

## 🏗️ Architecture

User → Streamlit UI → FastAPI → ML Model → Prediction

---

## 📂 Project Structure

````
app/
  ├── main.py        # FastAPI app
  ├── routes.py      # API endpoints
  ├── schemas.py     # Request/response models
  ├── services.py    # Business logic
  └── app_ui.py      # Streamlit UI

model/
  ├── loader.py      # Loads ML pipeline
  └── *.pkl          # Trained models

notebooks/
  └── training.ipynb

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
````

---

## ▶️ Run API

```bash
uvicorn app.main:app --reload
```

---

## 🎨 Run UI

```bash
streamlit run app/app_ui.py
```

---

## 📡 API Endpoint

POST `/predict`

```json
{
  "text": "I always fail"
}
```

Response:

```json
{
  "prediction": "catastrophizing",
  "confidence": 0.87
}
```

---

## 🧠 Tech Stack

* Python
* FastAPI
* Streamlit
* Scikit-learn
* Sentence Transformers

---

## 📌 Future Improvements

* Model explainability
* Multi-language support
* User history tracking
* Deployment (cloud)

---

## 👩‍💻 Author

Vanessa Duarte
