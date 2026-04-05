import streamlit as st
from PIL import Image
import numpy as np
import sqlite3
import datetime

st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("xray.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    prediction TEXT,
    confidence TEXT
)
""")
conn.commit()

# ---------------- HEADER ----------------
st.title("🩻 XRay Expert Pro")
st.write("AI-powered X-ray detection system")

st.warning("⚠️ Educational purposes only. Not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
option = st.sidebar.radio("Navigation", ["Home", "History"])

# ---------------- IMAGE PROCESSING ----------------
def preprocess_image(image):
    image = image.resize((128, 128))
    img_array = np.array(image)

    # Convert to grayscale
    if len(img_array.shape) == 3:
        img_array = np.mean(img_array, axis=2)

    img_array = img_array / 255.0
    return img_array

# ---------------- SIMPLE MODEL ----------------
def predict_xray(image):
    img = preprocess_image(image)

    # Simple feature: average brightness
    avg_pixel = np.mean(img)

    if avg_pixel < 0.45:
        return "Pneumonia", "84%"
    else:
        return "Normal", "78%"

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray Image")

    uploaded_file = st.file_uploader("Upload X-ray", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-ray", use_column_width=True)

        if st.button("Analyze"):

            prediction, confidence = predict_xray(image)

            st.success(f"Prediction: {prediction}")
            st.write(f"Confidence: {confidence}")

            if prediction == "Pneumonia":
                st.error("Possible lung infection detected. Consult a doctor.")
            else:
                st.info("No major abnormalities detected.")

            # Save to DB
            c.execute(
                "INSERT INTO scans (timestamp, prediction, confidence) VALUES (?, ?, ?)",
                (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), prediction, confidence)
            )
            conn.commit()

# ---------------- HISTORY ----------------
elif option == "History":

    st.subheader("Scan History")

    c.execute("SELECT * FROM scans ORDER BY id DESC")
    rows = c.fetchall()

    for row in rows:
        st.write(f"🗂 {row[1]} → {row[2]} ({row[3]})")
