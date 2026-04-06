from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Inicializar app
app = FastAPI()

# Cargar modelos
clf = joblib.load("classifier.pkl")
model = joblib.load("embedding_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Input schema
class TextInput(BaseModel):
    text: str

# Ruta de prueba
@app.get("/")
def home():
    return {"message": "API working 🚀"}

# Ruta de predicción
@app.post("/predict")
def predict(input: TextInput):
    embedding = model.encode([input.text])
    prediction = clf.predict(embedding)
    label = label_encoder.inverse_transform(prediction)

    return {"prediction": label[0]}