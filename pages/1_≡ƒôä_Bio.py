import base64
from pathlib import Path
import streamlit as st
from utils import header

st.set_page_config(page_title="Bio", page_icon="📄", layout="wide")
header("Bio", "Professional summary")

img = Path(__file__).parent.parent / "assets" / "profile.png"
left, right = st.columns([1, 3])
with left:
    if img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode()
        # st.image has no alt parameter, so render an <img> tag with real alt-text
        st.markdown(f'<img src="data:image/png;base64,{b64}" width="100%" '
                    'alt="Profile photo placeholder showing the owner\'s initials on a blue background">',
                    unsafe_allow_html=True)
        st.caption("Profile image (replace assets/profile.png with your photo).")
with right:
    st.markdown(
        "I am a computer science student at MSU Denver and a remote contractor with DataAnnotation, "
        "where I review and evaluate AI model outputs. I work mostly in Python, Java, and JavaScript, "
        "and I have a basic background in machine learning. I am interested in turning raw data into "
        "clear, honest visuals that help people make sense of patterns. This portfolio uses daily "
        "Seattle weather data to practice exploratory analysis and dashboard design with Streamlit and Plotly."
    )
st.subheader("Highlights")
st.markdown(
    "- Computer science coursework at MSU Denver, including data science and machine learning topics\n"
    "- Tools: Python, Pandas, Plotly, Streamlit, Git/GitHub\n"
    "- Also experienced in Java, JavaScript, and web development\n"
    "- Professional experience evaluating AI-generated content as a remote contractor\n"
    "- Built this app end to end: data cleaning, EDA, dashboard, and deployment"
)
st.subheader("Visualization philosophy")
st.markdown(
    "**Clarity first:** every chart answers one question and has a plain-language title. "
    "**Accessible by default:** color-blind-safe palettes, labeled axes with units, and text alternatives. "
    "**Honest scales:** no truncated bars, and I describe what the data shows without claiming causes."
)
