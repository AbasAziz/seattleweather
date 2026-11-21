# Seattle Weather Explorer

A multipage Streamlit portfolio app that explores four years of daily Seattle weather through an annotated EDA gallery and an interactive dashboard. It exists to practice clear, accessible, honest data visualization.

## Author
[Your Name] | [your-email@example.com] | [LinkedIn URL]

## App Navigation
- **Home (app.py):** overview and dataset snapshot
- **Bio:** professional summary, highlights, visualization philosophy
- **Charts Gallery:** six charts (line, bar, box, histogram, heatmap, scatter), each with a "How to read this chart" guide and observations
- **Dashboard:** date, weather-type, and temperature filters; four reactive KPIs; linked charts; insights
- **Future Work:** next steps and prototype-to-build reflection

## Dataset
- **Seattle Weather**, vega-datasets: https://github.com/vega/vega-datasets/blob/main/data/seattle-weather.csv
- **Records:** 1,461 daily rows (2012-01-01 to 2015-12-31)
- **Preprocessing:** none needed (no missing values); added `year` and `month` columns.
- This dataset contains no information about people, so no ethics note is required.

## Requirements
See `requirements.txt`. Run locally: `pip install -r requirements.txt && streamlit run app.py`

## Screenshots
Add 1-3 screenshots (for example `sample.png`) here.

## AI Assistance Acknowledgment
I used Claude (Anthropic) to help generate questions and draft code, which I reviewed and edited.
