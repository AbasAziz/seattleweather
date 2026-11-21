import streamlit as st
from utils import header

st.set_page_config(page_title="Future Work", page_icon="🧭", layout="wide")
header("Future Work", "What I would build next")
st.subheader("Next steps")
st.markdown(
    "1. **Forecasting:** add a simple seasonal model to predict temperature and rainfall, with uncertainty bands.\n"
    "2. **Data enrichment:** pull longer history from NOAA to test whether the 2012-2015 warming holds over decades.\n"
    "3. **Multi-city comparison:** add Denver and other cities to compare seasonal patterns.\n"
    "4. **Accessibility audit:** test with a screen reader and add downloadable data tables for every chart."
)
st.subheader("From paper prototype to final build")
st.markdown(
    "- Filters moved from the page body into a sidebar so charts stay visible while exploring.\n"
    "- The prototype's single chart grew into a six-chart gallery with plain-language guides.\n"
    "- KPI cards were added so every filter change has an immediate numeric effect."
)
