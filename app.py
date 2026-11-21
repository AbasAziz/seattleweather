import streamlit as st
from utils import header, load, SOURCE, SOURCE_NAME

st.set_page_config(page_title="Seattle Weather Portfolio", page_icon="🌦️", layout="wide")
header("Seattle Weather Explorer", "A data-visualization portfolio and mini analytics product")
df = load()
st.markdown(
    "Welcome! This multipage app explores **four years of daily Seattle weather** "
    "(2012-2015). Use the sidebar to move between pages."
)
c1, c2, c3 = st.columns(3)
c1.metric("Daily records", f"{len(df):,}")
c2.metric("Years covered", f"{df.year.nunique()}")
c3.metric("Variables", "6")
st.markdown(
    "- **Bio**: who I am and how I think about visualization\n"
    "- **Charts Gallery**: six annotated EDA charts\n"
    "- **Dashboard**: filter the data and watch KPIs and charts update\n"
    "- **Future Work**: what I would build next"
)
st.caption(f"Data: [{SOURCE_NAME}]({SOURCE}). Weather data only; no personal information.")
