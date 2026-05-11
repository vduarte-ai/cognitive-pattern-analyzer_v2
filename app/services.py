from app.routes import (
    embedding_model,
    classifier,
    label_encoder
)

from app.logger import logger


def analyze_text(text: str):

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