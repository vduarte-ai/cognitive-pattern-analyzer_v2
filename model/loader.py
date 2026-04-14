import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_pipeline():
    classifier_path = os.path.join(BASE_DIR, "model", "classifier.pkl")
    model_path = os.path.join(BASE_DIR, "model", "embedding_model.pkl")
    encoder_path = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
    
    classifier = joblib.load(classifier_path)
    embedding_model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)

    return classifier, embedding_model, label_encoder

classifier, embedding_model, label_encoder = load_pipeline()