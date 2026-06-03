import joblib
import json
from datetime import datetime

from app.database import SessionLocal
from app.models import Thought
from app.logger import logger


embedding_model = None
classifier = None
label_encoder = None

DISTORTION_EXPLANATIONS = {
    "catastrophizing":
        "This thought may assume the worst possible outcome.",

    "overgeneralization":
        "This thought may treat one negative event as a never-ending pattern.",

    "personalization":
        "This thought may take excessive responsibility for external events.",

    "black_and_white_thinking":
        "This thought may ignore nuance and see situations as all good or all bad.",

    "neutral":
        "No strong cognitive distortion detected."
}

REFRAMING_SUGGESTIONS = {
    "catastrophizing":
        "Try focusing on the most realistic outcome instead of the worst one.",

    "overgeneralization":
        "One difficult experience does not predict every future situation.",

    "personalization":
        "Not everything around you is caused by your actions.",

    "black_and_white_thinking":
        "Most situations exist somewhere between perfect and terrible.",

    "neutral":
        "Your thought appears relatively balanced."
}

EMOTION_KEYWORDS = {
    "anxiety": [
        "worried",
        "anxious",
        "scared",
        "fear",
        "panic"
    ],

    "sadness": [
        "sad",
        "hopeless",
        "empty",
        "depressed",
        "lonely"
    ],

    "anger": [
        "angry",
        "furious",
        "hate",
        "annoyed",
        "mad"
    ],

    "shame": [
        "worthless",
        "failure",
        "embarrassed",
        "ashamed",
        "stupid"
    ]
}

COMPANION_RESPONSES = {

    "catastrophizing":
        "It may help to slow down and focus on what is realistically happening right now.",

    "overgeneralization":
        "One difficult experience does not define your entire future.",

    "personalization":
        "You may be carrying responsibility that does not fully belong to you.",

    "black_and_white_thinking":
        "Things are often more nuanced than they initially appear.",

    "neutral":
        "Your reflection appears thoughtful and relatively balanced."
}

def interpret_confidence(score):
    if score >= 0.75:
        return "High confidence prediction"
    
    elif score >= 0.50:
        return "Moderate confidence prediction"
    
    else: 
        return "Low confidence prediction"
    
def detect_emotion(text):
    text = text.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "balanced"

def load_models():
    global embedding_model
    global classifier
    global label_encoder

    logger.info("STARTING MODEL LOAD")

    if embedding_model is None:
        logger.info("Loading embedding model...")
        embedding_model = joblib.load("model/embedding_model.pkl")
        logger.info("Embedding model loaded")

    if classifier is None:
        logger.info("Loading classifier...")
        classifier = joblib.load("model/classifier.pkl")
        logger.info("Classifier loaded")

    if label_encoder is None:
        logger.info("Loading label encoder...")
        label_encoder = joblib.load("model/label_encoder.pkl")
        logger.info("Label encoder loaded")

    logger.info("ALL MODELS LOADED")
    

def analyze_text(
        text: str,
        current_user: str
    ):
    logger.info("ANALYZE STARTED")
    
    load_models()
    logger.info("MODELS READY")

    embedding = embedding_model.encode([text])

    prediction = classifier.predict(embedding)
    probabilities = classifier.predict_proba(embedding)

    label = label_encoder.inverse_transform(prediction)[0]

    confidence = float(max(probabilities[0]))
    
    confidence_label = interpret_confidence(confidence)
    
    emotion = detect_emotion(text)

    labels = label_encoder.classes_
    probs = probabilities[0]

    all_probabilities = {
        label: float(prob)
        for label, prob in zip(labels, probs)
    }

    logger.info(f"Prediction: {label}")

    explanation = DISTORTION_EXPLANATIONS.get(
        label,
        "No explanation available."
    )
    
    reframing = REFRAMING_SUGGESTIONS.get(
        label,
        "No reframing suggestion available."
    )
    
    companion_response = COMPANION_RESPONSES.get(
        label,
        "Thank you for sharing your thoughs."
    )
    
    history_entry = {
        "text": text,
        "prediction": label,
        "confidence": confidence,
        "confidence_label": confidence_label,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat(),
        "user_email": current_user
    }
    
    save_history(history_entry)

    return {
        "prediction": label,
        "confidence": round(confidence, 3),
        "confidence_label": confidence_label,
        "all_probabilities": all_probabilities,
        "explanation": explanation,
        "reframing": reframing,
        "emotion": emotion,
        "companion_response": companion_response
    }
    
def save_history(entry):
    db = SessionLocal()
    
    thought = Thought(
        text=entry["text"],
        prediction=entry["prediction"],
        confidence=entry["confidence"],
        confidence_label=entry["confidence_label"],
        emotion=entry["emotion"],
        timestamp=entry["timestamp"],
        user_email=entry["user_email"]
    )
    
    db.add(thought)
    db.commit()
    db.close()