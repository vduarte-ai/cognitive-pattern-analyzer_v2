import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import SessionLocal
from models import Thought
import time

# Init ##
st.set_page_config(page_title="Cognitive Analyzer", page_icon="🧠")

st.markdown("""
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    .stTextArea textarea {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }

    .stButton button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }

    </style>
    """, unsafe_allow_html=True)


## Login ##
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "token" not in st.session_state:
    st.session_state.token = None
    
auth_mode = st.radio(
    "Authentication",
    ["Login", "Register"],
    horizontal=True
)

        
if  st.session_state.logged_in:
    col1, col2 = st.columns([4,1])

    with col2:
        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.token = None

            if "email" in st.session_state:
                del st.session_state["email"]

            st.rerun()
   
if  not st.session_state.logged_in: 
    if auth_mode == "Login":    
        # Login UI
        st.subheader("🔐 Login")

        email = st.text_input("Email")

        password = st.text_input(
           "Password",
           type="password"
        )

        if st.button("Login"):
            response = requests.post(
                "https://cognitive-pattern-analyzer-v2.onrender.com/login",
                json={
                    "email": email,
                    "password": password
                }
            )
    
            result = response.json()

            if response.status_code == 200:

                result = response.json()

                st.session_state.logged_in = True
                st.session_state.token = result["access_token"]
                st.session_state.email = email

                st.success("Login successful")
                st.rerun()
            
            else:

                st.error("Invalid credentials")
    
    elif auth_mode == "Register":
        st.subheader("📝 Create Account") 
        
        register_username = st.text_input(
             "Username",
              key="register_username"   
        )
        
        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Create Account"):
            start = time.time()
            response = requests.post(
                "https://cognitive-pattern-analyzer-v2.onrender.com/register",
                json={
                    "username": register_username,
                    "email": register_email,
                    "password": register_password
                }
            )
            
            

            print("Register took:", time.time() - start)

            if response.status_code == 200:

                st.success(
                    "Account created successfully. Please login."
                )

            else:

                st.error(
                    f"Registration failed: {response.text}"
                )
                
    if not st.session_state.logged_in:         
        st.warning("Please login to continue.")
        st.stop()
    
    

       
    

#
st.title("🧠 Cognitive Pattern Analyzer")
st.caption(
    "Analyze thought patterns, emotional distortions, and cognitive reframing."
)

text = st.text_area(
      "📝 Journal Entry",
    height=250,
    placeholder="Write freely about your thoughts, emotions, or experiences..."
)

if st.button("Analyze"):

    if not text.strip():
        st.warning("Please enter some text.")
    
    else:

        with st.spinner("Analyzing cognitive patterns..."):

            try:

                response = requests.post(
                    "https://cognitive-pattern-analyzer-v2.onrender.com/predict",
                    json={"text": text},
                    headers={
                        "Authorization":
                            f"Bearer {st.session_state.token}"
                            },
                )

                st.write("STATUS:", response.status_code)
                st.write("RESPONSE:")
                st.code(response.text)

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
                    
                    st.subheader("Explanation")
                    st.info(result["explanation"])
                    
                    st.subheader("Reframing Suggestion")
                    st.success(result["reframing"])
                    
                    st.subheader("AI Reflection")
                    st.info(result["companion_response"])

                    st.write(f"{confidence:.2f}")
                    st.caption(result["confidence_label"])
                    
                    st.subheader("Detected Emotion")
                    st.info(result["emotion"])

                    st.subheader("All Probabilities")

                    for label, prob in probabilities.items():
                        st.write(f"**{label}**")
                        st.progress(prob)

                else:
                    st.error("Prediction failed.")
                    
                    st.write("STATUS:", response.status_code)
                    st.write("RESPONSE:", response.text)

            except Exception as e:
                st.exception(e)
                
    
st.subheader("Recent Thought History")

if st.button("🗑 Clear History"):

    with open("data/history.json", "w") as file:
        json.dump([], file)

    st.success("History cleared.")

try:
    db = SessionLocal()
    
    history = (
        db.query(Thought)
        .filter(Thought.user_email == st.session_state.email)
        .order_by(Thought.id.desc())
        .limit(5)
        .all()
    )
    
    db.close()

    for item in history:

        st.write(f"**Thought:** {item.text}")
        st.write(f"**Prediction:** {item.prediction}")
        st.write(f"**Confidence:** {item.confidence}")

        confidence_label = item.confidence_label

        st.caption(confidence_label)
        
        formatted_time = datetime.fromisoformat(
            item.timestamp
        ).strftime("%Y-%m-%d %H:%M")
        st.caption(f"🕒 {formatted_time}")

        st.write("---")

    st.subheader("Distortion Analytics")

    if history:

        df = pd.DataFrame([
            {
                "text": item.text,
                "prediction": item.prediction,
                "confidence": item.confidence,
                "confidence_label": item.confidence_label,
                "emotion": item.emotion,
                "timestamp": item.timestamp
            }
            for item in history
        ])

        counts = df["prediction"].value_counts()

        chart_data = counts.reset_index()
        chart_data.columns = ["Pattern", "Count"]
        
        fig = px.bar(
            chart_data,
            x="Pattern",
            y="Count",
            title="Cognitive Distortion Trends"
            )

        st.plotly_chart(fig)
        
        timeline_df = pd.DataFrame([
            {
                "timestamp": item.timestamp,
                "prediction": item.prediction
            }
            for item in history
        ])
        
        timeline_df["timestamp"] = pd.to_datetime(
            timeline_df["timestamp"]
        )
        
        timeline_counts = (
            timeline_df
            .groupby("prediction")
            .size()
            .reset_index(name="count")
        )
        
        timeline_fig = px.pie(
            timeline_counts,
            values="count",
            names="prediction",
            title="Though Distribution"
        )
        
        st.plotly_chart(timeline_fig)
        
        most_common = counts.idxmax()
        st.subheader("Trend Insight")
        
        if most_common == "catastrophizing":
            st.warning(
                "Recent thoughts frequently assume worst-case outcomes."
            )
        elif most_common == "overgeneralization":
            st.warning(
                "Recent thoughts may be turning isolated events into broad conclusions."
            )
        elif most_common == "personalization":
            st.warning(
                "Recent thoughst may involve excessive self-blame."
            )
        else:
            st.success(
                "Recent thought patterns appear relavively balanced."
            )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download History CSV",
            data=csv,
            file_name="thought_history.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error("Could not load history.")