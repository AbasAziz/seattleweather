import pandas as pd
import plotly.express as px
import streamlit as st
from utils import header, load, style, refreshed, ORDER, PAL, SOURCE, SOURCE_NAME

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
header("Dashboard", "Filter the data; KPIs and charts update together")
df = load()

# ---- Filters (sidebar) ----
lo, hi = df.date.min().date(), df.date.max().date()
dr = st.sidebar.date_input("Date range", (lo, hi), min_value=lo, max_value=hi)
types = st.sidebar.multiselect("Weather type", ORDER, default=ORDER)
t_lo, t_hi = float(df.temp_max.min()), float(df.temp_max.max())
tmin, tmax = st.sidebar.slider("Daily high (°C)", t_lo, t_hi, (t_lo, t_hi))
if len(dr) != 2:
    st.info("Select an end date to apply the date filter.")
    st.stop()
f = df[(df.date >= pd.Timestamp(dr[0])) & (df.date <= pd.Timestamp(dr[1]))
       & df.weather.isin(types) & df.temp_max.between(tmin, tmax)]
if f.empty:
    st.warning("No days match these filters. Widen the filters to see results.")
    st.stop()

# ---- KPIs ----
k = st.columns(4)
k[0].metric("Days selected", f"{len(f):,}")
k[1].metric("Avg daily high", f"{f.temp_max.mean():.1f} °C")
k[2].metric("Total precipitation", f"{f.precipitation.sum():,.0f} mm")
k[3].metric("Windiest day", f"{f.wind.max():.1f} m/s")

# ---- Linked visuals ----
m = f.groupby(pd.Grouper(key="date", freq="MS")).agg(
    avg_high=("temp_max", "mean"), precip=("precipitation", "sum"), days=("date", "count")).reset_index()
m = m[m.days > 0]
c1, c2 = st.columns(2)
f1 = px.line(m, x="date", y="avg_high", markers=True, color_discrete_sequence=["#D55E00"],
             labels={"date": "Month", "avg_high": "Average daily high (°C)"},
             title="Average daily high by month (selected days)")
c1.plotly_chart(style(f1, 380), width="stretch")
cnt = f.weather.value_counts().reindex(ORDER).dropna().reset_index()
cnt.columns = ["weather", "Days"]
f2 = px.bar(cnt, x="weather", y="Days", color="weather", color_discrete_map=PAL,
            labels={"weather": "Weather type"}, title="Days per weather type (selected days)")
f2.update_layout(showlegend=False)
c2.plotly_chart(style(f2, 380), width="stretch")
f3 = px.bar(m, x="date", y="precip", color_discrete_sequence=["#0072B2"],
            labels={"date": "Month", "precip": "Total precipitation (mm)"},
            title="Monthly precipitation (selected days)")
st.plotly_chart(style(f3, 340), width="stretch")

# ---- Narrative ----
st.subheader("Insights")
st.markdown(
    "- Temperature and precipitation swing seasonally: warm, dry summers and cool, wet winters.\n"
    "- Try selecting only **snow**: those days are cold (average high near 6 °C) and relatively windy.\n"
    "- Filtering to **sun** shows the warmest days, but sunny days also appear in every month.\n"
    "- Fog days become more common in later years; narrow the date range to 2015 to see it.\n"
    "- **Limitations:** one city, four years, and weather labels are single categories per day. "
    "These are descriptive patterns, not causal explanations or climate trends."
)
st.markdown(f"[![Data source](https://img.shields.io/badge/data-Seattle%20Weather-blue)]({SOURCE})")
st.caption(f"Last refreshed: {refreshed()} | Source: [{SOURCE_NAME}]({SOURCE})")
