import streamlit as st
from PIL import Image
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- DARK MODE ----------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    bg_color = "#0E1117"
    text_color = "white"
    card_color = "#1c1f26"
else:
    bg_color = "#f5f7fb"
    text_color = "black"
    card_color = "white"

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
.main {{
    background-color: {bg_color};
    color: {text_color};
}}
.card {{
    padding: 20px;
    border-radius: 15px;
    background-color: {card_color};
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}}
.title {{
    text-align: center;
    color: #0B3D91;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='title'>🩻 XRay Expert Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered X-ray insights & report assistant</p>", unsafe_allow_html=True)

st.warning("⚠️ This tool is for educational purposes only and not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ["Home", "History", "About"])

# ---------------- FAKE AI ----------------
def analyze_xray():
    return {
        "findings": "Mild irregular opacity detected in lung region.",
        "issues": "Possible early-stage infection or inflammation.",
        "explanation": "The scan shows slight variations in tissue density which may indicate minor abnormalities.",
        "recommendation": "Consult a radiologist for further evaluation.",
        "confidence": "78%"
    }

# ---------------- PDF GENERATION ----------------
def create_pdf(result):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("XRay Expert Pro - Report", styles['Title']))
    content.append(Spacer(1, 10))

    for key, value in result.items():
        content.append(Paragraph(f"<b>{key.capitalize()}:</b> {value}", styles['Normal']))
        content.append(Spacer(1, 8))

    doc.build(content)
    return "report.pdf"

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray or Medical Report")

    uploaded_file = st.file_uploader("Upload Image or Report", type=["jpg", "png", "jpeg", "pdf"])

    if uploaded_file:

        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded X-ray", use_column_width=True)

        if st.button("🔍 Analyze Scan"):

            with st.spinner("Analyzing..."):

                result = analyze_xray()
                st.success("Analysis Complete")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"<div class='card'><h4>🧠 Findings</h4><p>{result['findings']}</p></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card'><h4>⚠️ Issues</h4><p>{result['issues']}</p></div>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<div class='card'><h4>📋 Explanation</h4><p>{result['explanation']}</p></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card'><h4>📌 Recommendation</h4><p>{result['recommendation']}</p></div>", unsafe_allow_html=True)

                st.progress(int(result["confidence"].replace("%", "")))
                st.write(f"📊 Confidence Score: {result['confidence']}")

                # PDF download
                pdf_file = create_pdf(result)
                with open(pdf_file, "rb") as f:
                    st.download_button("📄 Download Report", f, file_name="xray_report.pdf")

                # Save history
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
    **XRay Expert Pro** is an AI-inspired tool designed to help users understand X-ray scans and reports.

    ### Features:
    - Upload X-rays  
    - Smart AI-style analysis  
    - PDF report download  
    - Dark mode  
    - Scan history  

    ---
    Developed by Humna Imran
    """)
