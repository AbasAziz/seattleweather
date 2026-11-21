"""Shared helpers: data loading (cached), color-blind-safe palette, branding."""
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import streamlit as st

OWNER = "[Your Name]"                                   # TODO: replace
CONTACT = "[your-email@example.com] | [LinkedIn URL]"   # TODO: replace
SOURCE_NAME = "Seattle Weather (vega-datasets)"
SOURCE = "https://github.com/vega/vega-datasets/blob/main/data/seattle-weather.csv"
ORDER = ["sun", "rain", "drizzle", "fog", "snow"]
# Okabe-Ito color-blind-safe palette
PAL = {"sun": "#E69F00", "rain": "#0072B2", "drizzle": "#56B4E9", "fog": "#999999", "snow": "#CC79A7"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


@st.cache_data
def load() -> pd.DataFrame:
    """Load the CSV once; add year/month helper columns."""
    df = pd.read_csv(Path(__file__).parent / "data" / "seattle-weather.csv", parse_dates=["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


@st.cache_data
def refreshed() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def header(title: str, subtitle: str):
    st.title(title)
    st.caption(f"{subtitle}  |  {OWNER}  |  {CONTACT}")


def style(fig, height=420):
    fig.update_layout(template="plotly_white", height=height, font=dict(size=14),
                      margin=dict(l=10, r=10, t=60, b=10))
    return fig
