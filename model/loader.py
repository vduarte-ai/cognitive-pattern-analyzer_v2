import joblib

def load_model():
    clf = joblib.load("model/classifier.pkl")
    encoder = joblib.load("model/embedding_model.pkl")
    return clf, encoder