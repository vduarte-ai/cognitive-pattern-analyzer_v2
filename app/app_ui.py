import streamlit as st
import requests

st.set_page_config(page_title="Cognitive Analyzer", page_icon="🧠")

st.title("🧠 Cognitive Pattern Analyzer")
st.write("Detect cognitive distortions in your thoughts")

text = st.text_area("Enter your thought:")

if st.button("Analyze"):
    if text:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={"text": text}
        )

        result = response.json()

        st.success(f"Prediction: {result['prediction']}")
        st.metric("Confidence", f"{result['confidence']:.2f}")