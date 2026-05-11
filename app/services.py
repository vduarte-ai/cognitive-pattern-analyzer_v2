import joblib

from app.logger import logger


embedding_model = None
classifier = None
label_encoder = None


def load_models():
    global embedding_model
    global classifier
    global label_encoder

    if embedding_model is None:
        logger.info("Loading embedding model...")
        embedding_model = joblib.load("model/embedding_model.pkl")

    if classifier is None:
        logger.info("Loading classifier...")
        classifier = joblib.load("model/classifier.pkl")

    if label_encoder is None:
        logger.info("Loading label encoder...")
        label_encoder = joblib.load("model/label_encoder.pkl")


def analyze_text(text: str):

    load_models()

    embedding = embedding_model.encode([text])

    prediction = classifier.predict(embedding)
    probabilities = classifier.predict_proba(embedding)

    label = label_encoder.inverse_transform(prediction)[0]

    confidence = float(max(probabilities[0]))

    labels = label_encoder.classes_
    probs = probabilities[0]

    all_probabilities = {
        label: float(prob)
        for label, prob in zip(labels, probs)
    }

    logger.info(f"Prediction: {label}")

    return {
        "prediction": label,
        "confidence": round(confidence, 3),
        "all_probabilities": all_probabilities
    }