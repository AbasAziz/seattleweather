import pandas as pd
import plotly.express as px
import streamlit as st
from utils import header, load, style, ORDER, PAL, MONTHS, SOURCE, SOURCE_NAME

st.set_page_config(page_title="Charts Gallery", page_icon="📊", layout="wide")
header("EDA Gallery", "Six charts, each answering one question")
df = load()


def block(n, question, fig, how, obs):
    """Render one gallery entry: question, chart, caption, how-to-read, observations."""
    st.subheader(f"{n}. {question}")
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Source: [{SOURCE_NAME}]({SOURCE}), daily records 2012-2015.")
    a, b = st.columns(2)
    a.markdown("**How to read this chart**\n" + "\n".join(f"- {h}" for h in how))
    b.markdown("**What the data shows**\n" + "\n".join(f"- {o}" for o in obs))
    st.divider()


# 1. Line (interactive: hover, zoom, range slider)
roll = df.set_index("date")[["temp_max", "temp_min"]].rolling(30).mean().dropna().reset_index()
roll = roll.melt("date", var_name="Series", value_name="Temperature (°C)")
roll["Series"] = roll["Series"].map({"temp_max": "Daily high", "temp_min": "Daily low"})
f1 = px.line(roll, x="date", y="Temperature (°C)", color="Series",
             color_discrete_map={"Daily high": "#D55E00", "Daily low": "#0072B2"},
             title="30-day rolling average temperature, 2012-2015")
f1.update_xaxes(rangeslider_visible=True, title="Date")
block(1, "Has Seattle gotten warmer between 2012 and 2015?", style(f1),
      ["X axis is time; Y axis is temperature in °C, averaged over the previous 30 days to smooth noise.",
       "Orange is the daily high, blue is the daily low. Hover for exact values; drag the slider below to zoom.",
       "Look for the repeating yearly wave and whether each peak is higher than the last."],
      ["Temperature follows a strong yearly cycle, peaking each July-August and bottoming in winter.",
       "Average daily highs by year rose from 15.3 °C (2012) to 16.1, 17.0, and 17.4 °C (2015).",
       "Four years is too short to call this a climate trend; it may simply be year-to-year variation."])

# 2. Bar (interactive: toggle)
mode = st.radio("Bar layout", ["group", "stack"], horizontal=True,
                format_func=lambda m: "Side by side" if m == "group" else "Stacked")
cnt = df.groupby(["year", "weather"]).size().reset_index(name="Days")
f2 = px.bar(cnt, x="year", y="Days", color="weather", barmode=mode, color_discrete_map=PAL,
            category_orders={"weather": ORDER}, title="Number of days per weather type, by year")
f2.update_xaxes(type="category", title="Year")
block(2, "How does the mix of weather types change from year to year?", style(f2),
      ["Each bar group is one year; bar height is the number of days with that weather label.",
       "Colors are color-blind-safe and match across the whole app.",
       "Compare the same color across years to see growth or decline."],
      ["Rain leads only in 2012 (191 days); from 2013 on, sun is the most common label, and rain days fall to 144 by 2015.",
       "Fog days climb every year: 5, 16, 28, then 52.",
       "Snow drops from 21 days in 2012 to none in 2015, and drizzle nearly disappears after 2013."])

# 3. Box
f3 = px.box(df, x="weather", y="temp_max", color="weather", color_discrete_map=PAL,
            category_orders={"weather": ORDER}, points="outliers",
            labels={"weather": "Weather type", "temp_max": "Daily high (°C)"},
            title="Daily high temperature by weather type")
f3.update_layout(showlegend=False)
block(3, "How do daily high temperatures differ across weather types?", style(f3),
      ["Each box covers the middle 50% of days; the line inside is the median.",
       "Whiskers show the typical range; dots are unusual days.",
       "Boxes that barely overlap mean the weather types separate clearly on temperature."],
      ["Sun days are warmest on average (19.9 °C); snow days are far colder (5.6 °C).",
       "Rain days average 13.5 °C, cooler than fog (16.8 °C) or drizzle (15.9 °C).",
       "Sun, fog, and drizzle overlap heavily, so temperature alone cannot tell them apart."])

# 4. Histogram (interactive: variable, bins, zero filter)
opts = {"Precipitation (mm)": "precipitation", "Wind speed (m/s)": "wind", "Daily high (°C)": "temp_max"}
c1, c2, c3 = st.columns(3)
label = c1.selectbox("Variable", list(opts))
bins = c2.slider("Number of bins", 10, 60, 30)
skip0 = c3.checkbox("Exclude zero-precipitation days", value=True) if opts[label] == "precipitation" else False
d4 = df[df.precipitation > 0] if skip0 else df
f4 = px.histogram(d4, x=opts[label], nbins=bins, color_discrete_sequence=["#0072B2"],
                  labels={opts[label]: label}, title=f"Distribution of {label.lower()}")
f4.update_yaxes(title="Number of days")
block(4, "What does the typical day look like for each measurement?", style(f4),
      ["X axis is the measurement in 'bins'; Y axis is how many days fall in each bin.",
       "Tall bars are common values; long thin tails are rare extremes.",
       "Change the variable and bin count above to see how the shape changes."],
      ["57% of days had no precipitation at all, so the raw precipitation histogram is dominated by zero.",
       "Among wet days, most are light, with a long tail up to 55.9 mm (2015-03-15).",
       "Wind and temperature are roughly bell-shaped; wind is slightly skewed toward high values."])

# 5. Heatmap
pv = df.pivot_table(index="month", columns="year", values="precipitation", aggfunc="sum")
pv.index = MONTHS
f5 = px.imshow(pv, text_auto=".0f", color_continuous_scale="Blues", aspect="auto",
               labels=dict(x="Year", y="Month", color="Total precipitation (mm)"),
               title="Total monthly precipitation (mm)")
f5.update_xaxes(type="category")
block(5, "Which months are rainiest, and does the pattern repeat each year?", style(f5, 520),
      ["Rows are months, columns are years; each cell is that month's total precipitation in mm.",
       "Darker blue means more precipitation; numbers are printed in each cell.",
       "Scan down a column for the seasonal pattern and across a row for year-to-year change."],
      ["Wet season runs roughly October-March; summed over all four years, November (642 mm) and December (623 mm) lead.",
       "July is the driest month (48 mm in total across four years).",
       "The pattern repeats, but amounts vary: 2013 was drier overall (828 mm) than 2012 or 2014 (about 1,230 mm)."])

# 6. Scatter (interactive: hover)
f6 = px.scatter(df, x="temp_min", y="temp_max", color="weather", color_discrete_map=PAL,
                category_orders={"weather": ORDER}, opacity=0.65, hover_data=["date", "precipitation", "wind"],
                labels={"temp_min": "Daily low (°C)", "temp_max": "Daily high (°C)", "weather": "Weather"},
                title="Daily high vs. daily low temperature")
block(6, "How closely do daily highs and lows move together?", style(f6),
      ["Each dot is one day; X is the daily low, Y is the daily high (both °C).",
       "Dots climbing from lower-left to upper-right mean the two rise together.",
       "Color shows weather type; hover a dot for the date, rain, and wind."],
      ["Highs and lows are strongly related (correlation 0.88).",
       "Snow days cluster in the lower-left; sun days dominate the upper-right.",
       "Hover over outlying dots to inspect individual days with unusual high/low combinations."])
