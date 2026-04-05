import streamlit as st
from PIL import Image
import base64
import openai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="XRay Expert Pro", layout="wide")

# ---------------- API KEY ----------------
# Put your OpenAI API key in Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align: center; color: #0B3D91;'>🩻 XRay Expert Pro</h1>
    <p style='text-align: center;'>AI-powered X-ray insights & report assistant</p>
""", unsafe_allow_html=True)

st.warning("⚠️ This tool is for educational purposes only and not a medical diagnosis.")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ["Home", "History", "About"])

# ---------------- FUNCTION: AI ANALYSIS ----------------
def analyze_with_ai(text_input):
    prompt = f"""
    You are a medical assistant AI.

    Analyze the following X-ray or medical report description and provide:
    1. Key findings
    2. Possible issues
    3. Simple explanation
    4. Recommended next steps

    Input:
    {text_input}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response['choices'][0]['message']['content']

# ---------------- HOME ----------------
if option == "Home":

    st.subheader("Upload X-ray or Medical Report")

    uploaded_file = st.file_uploader("Upload Image or Report", type=["jpg", "png", "jpeg", "pdf", "txt"])

    user_text = ""

    if uploaded_file:

        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            user_text = "X-ray image uploaded. Analyze possible abnormalities."

        else:
            user_text = uploaded_file.read().decode("utf-8", errors="ignore")
            st.text_area("Extracted Text", user_text, height=200)

        if st.button("Analyze with AI"):

            with st.spinner("Analyzing with AI..."):

                result = analyze_with_ai(user_text)

                st.success("Analysis Complete")

                st.markdown("### 🧠 AI Analysis")
                st.write(result)

                # Save history
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append(result)

# ---------------- HISTORY ----------------
elif option == "History":

    st.subheader("Previous Analyses")

    if "history" in st.session_state and st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            st.write(f"### Scan {i+1}")
            st.write(item)
    else:
        st.info("No history available")

# ---------------- ABOUT ----------------
elif option == "About":

    st.subheader("About XRay Expert Pro")

    st.write("""
    XRay Expert Pro is an AI-powered tool designed to assist users in understanding X-ray images and medical reports.

    Features:
    - Upload X-rays or reports
    - AI-based insights using GPT
    - Simple explanations
    - Scan history tracking

    Developed by Humna Imran
    """)
