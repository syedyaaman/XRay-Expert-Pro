import streamlit as st
from PIL import Image
import datetime

st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.title {
    text-align: center;
    color: #0B3D91;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='title'>🩻 XRay Expert Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered X-ray insights & report assistant</p>", unsafe_allow_html=True)

st.warning("⚠️ This tool is for educational purposes only and not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ["Home", "History", "About"])

# ---------------- FAKE AI ENGINE ----------------
def analyze_xray():
    return {
        "findings": "Mild irregular opacity detected in lung region.",
        "issues": "Possible early-stage infection or inflammation.",
        "explanation": "The scan shows slight variations in tissue density which may indicate minor abnormalities.",
        "recommendation": "Consult a radiologist for further evaluation and confirmatory tests."
    }

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray or Medical Report")

    uploaded_file = st.file_uploader("Upload Image or Report", type=["jpg", "png", "jpeg", "pdf"])

    if uploaded_file:

        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded X-ray", use_column_width=True)

        if st.button("🔍 Analyze Scan"):

            with st.spinner("Analyzing scan..."):

                result = analyze_xray()
                st.success("Analysis Complete")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"<div class='card'><h4>🧠 AI Findings</h4><p>{result['findings']}</p></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card'><h4>⚠️ Possible Issues</h4><p>{result['issues']}</p></div>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<div class='card'><h4>📋 Explanation</h4><p>{result['explanation']}</p></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card'><h4>📌 Recommendation</h4><p>{result['recommendation']}</p></div>", unsafe_allow_html=True)

                # Save history with timestamp
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append({
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "result": result
                })

# ---------------- HISTORY ----------------
elif option == "History":

    st.subheader("📜 Scan History")

    if "history" in st.session_state and st.session_state.history:

        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"### 🗂 Scan {i+1} ({item['time']})")

            st.markdown(f"<div class='card'><b>Findings:</b> {item['result']['findings']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><b>Issues:</b> {item['result']['issues']}</div>", unsafe_allow_html=True)

    else:
        st.info("No previous scans available")

# ---------------- ABOUT ----------------
elif option == "About":

    st.subheader("About XRay Expert Pro")

    st.markdown("""
    **XRay Expert Pro** is an AI-inspired application designed to help users understand X-ray scans and medical reports in a simple way.

    ### 🔍 Features:
    - Upload X-ray images or reports  
    - Smart AI-style analysis  
    - Clean and professional interface  
    - Scan history tracking  

    ### ⚠️ Disclaimer:
    This tool does not replace professional medical advice.

    ---
    **Developed by Humna Imran**
    """)
