import streamlit as st
from PIL import Image
import sqlite3
import datetime
import numpy as np
import os

st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("xray.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    result TEXT
)
""")
conn.commit()

# ---------------- HEADER ----------------
st.title("🩻 XRay Expert Pro")
st.write("AI-powered X-ray insights & report assistant")

st.warning("⚠️ Educational purposes only. Not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
option = st.sidebar.radio("Navigation", ["Home", "History"])

# ---------------- FAKE MODEL ----------------
def predict_xray(image):
    # Simulating model using random logic
    value = np.random.rand()

    if value > 0.5:
        return {
            "label": "Pneumonia",
            "confidence": "82%",
            "details": "Possible lung infection detected."
        }
    else:
        return {
            "label": "Normal",
            "confidence": "76%",
            "details": "No major abnormalities detected."
        }

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-ray", use_column_width=True)

        if st.button("Analyze"):

            result = predict_xray(image)

            st.success(f"Prediction: {result['label']}")
            st.write(f"Confidence: {result['confidence']}")
            st.write(result["details"])

            # Save to DB
            c.execute("INSERT INTO scans (timestamp, result) VALUES (?, ?)",
                      (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), result['label']))
            conn.commit()

# ---------------- HISTORY ----------------
elif option == "History":

    st.subheader("Scan History")

    c.execute("SELECT * FROM scans ORDER BY id DESC")
    data = c.fetchall()

    for row in data:
        st.write(f"🗂 {row[1]} → {row[2]}")
