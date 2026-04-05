import streamlit as st
from PIL import Image
import pytesseract
import numpy as np

st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align: center; color: #0B3D91;'>🩻 XRay Expert Pro</h1>
    <p style='text-align: center;'>AI-powered X-ray insights & report assistant</p>
""", unsafe_allow_html=True)

st.warning("⚠️ This tool is for educational purposes only and not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ["Home", "History", "About"])

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray or Medical Report")

    uploaded_file = st.file_uploader("Upload Image or Report", type=["jpg", "png", "jpeg", "pdf"])

    if uploaded_file:

        # Show image preview if image
        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze"):

            with st.spinner("Analyzing..."):

                # Fake AI logic (replace later with real model)
                findings = "Possible signs of abnormality detected."
                issues = "Potential infection or inflammation."
                explanation = "The uploaded scan shows patterns that may indicate irregular tissue density."
                recommendation = "Consult a certified radiologist for further evaluation."

                st.success("Analysis Complete")

                col1, col2 = st.columns(2)

                with col1:
                    st.info("🧠 AI Findings")
                    st.write(findings)

                    st.warning("⚠️ Possible Issues")
                    st.write(issues)

                with col2:
                    st.success("📋 Explanation")
                    st.write(explanation)

                    st.error("📌 Recommendation")
                    st.write(recommendation)

                # Save history
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append({
                    "findings": findings,
                    "issues": issues
                })

# ---------------- HISTORY ----------------
elif option == "History":

    st.subheader("Previous Analyses")

    if "history" in st.session_state and st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            st.write(f"### Scan {i+1}")
            st.write("Findings:", item["findings"])
            st.write("Issues:", item["issues"])
    else:
        st.info("No history available")

# ---------------- ABOUT ----------------
elif option == "About":

    st.subheader("About XRay Expert Pro")

    st.write("""
    XRay Expert Pro is an AI-powered tool designed to assist users in understanding X-ray images and medical reports.

    Features:
    - Upload X-rays or reports
    - AI-based insights
    - Simple explanations
    - Scan history tracking

    Developed by Humna Imran
    """)
