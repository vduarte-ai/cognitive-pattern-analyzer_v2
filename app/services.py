from model.loader import load_model

clf, encoder = load_model()

def predict_text(text):
    embedding = encoder.encode([text])
    prediction = clf.predict(embedding)
    return {"prediction": prediction[0]}