import streamlit as st
import requests

st.set_page_config(page_title="Cognitive Analyzer", page_icon="🧠")

st.title("🧠 Cognitive Pattern Analyzer")
st.markdown("Analyze your thoughts and detect cognitive distortions.")

text = st.text_area("💭 Enter your thought:")

if st.button("Analyze"):

    if not text.strip():
        st.warning("Please enter some text.")
    
    else:

        with st.spinner("Analyzing cognitive patterns..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json={"text": text}
                )

                result = response.json()

                if response.status_code == 200 and result["success"]:

                    prediction = result["prediction"]
                    confidence = result["confidence"]
                    probabilities = result["all_probabilities"]

                    st.success("Analysis complete")

                    st.subheader("Detected Pattern")
                    st.error(f"⚠️ {prediction}")

                    st.subheader("Confidence")
                    st.progress(confidence)

                    st.write(f"{confidence:.2f}")

                    st.subheader("All Probabilities")

                    for label, prob in probabilities.items():
                        st.write(f"**{label}**")
                        st.progress(prob)

                else:
                    st.error("Prediction failed.")

            except Exception as e:
                st.exception(e)