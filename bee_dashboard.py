import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "bee_log.csv"

st.set_page_config(page_title="Beekeeping Dashboard", page_icon="🐝")

st.title("🐝 Beekeeping Dashboard V2")

columns = [
    "Date", "Hive", "Queen Seen", "Queen Notes", "Brood Pattern",
    "Hive Strength", "Temperament", "Mite Count", "Feed Added",
    "Honey Harvested", "Weather", "Notes", "Next Action",
    "Next Inspection"
]

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=columns)

st.header("Add Hive Inspection")

with st.form("inspection_form"):
    hive = st.selectbox("Hive", ["Main Hive", "Orchard Hive", "New Split", "Other"])
    inspection_date = st.date_input("Inspection date", date.today())

    queen_seen = st.selectbox("Queen seen?", ["Yes", "No", "Not sure"])
    queen_notes = st.text_input("Queen notes", "Good laying pattern")

    brood = st.selectbox("Brood pattern", ["Excellent", "Good", "Spotty", "Weak", "None"])
    strength = st.slider("Hive strength", 1, 10, 7)

    temperament = st.selectbox("Temperament", ["Calm", "Normal", "Spicy", "Mean"])
    mite_count = st.number_input("Mite count", min_value=0, step=1)

    feed = st.text_input("Feed added", "None")
    honey = st.number_input("Honey harvested - quarts", min_value=0.0, step=0.25)

    weather = st.text_input("Weather", "Sunny")
    notes = st.text_area("Notes")
    next_action = st.text_input("Next action", "Check again soon")
    next_inspection = st.date_input("Next inspection date")

    submitted = st.form_submit_button("Save Inspection")

    if submitted:
        new_row = {
            "Date": inspection_date,
            "Hive": hive,
            "Queen Seen": queen_seen,
            "Queen Notes": queen_notes,
            "Brood Pattern": brood,
            "Hive Strength": strength,
            "Temperament": temperament,
            "Mite Count": mite_count,
            "Feed Added": feed,
            "Honey Harvested": honey,
            "Weather": weather,
            "Notes": notes,
            "Next Action": next_action,
            "Next Inspection": next_inspection
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Inspection saved!")

st.header("Hive Log")
st.dataframe(df, use_container_width=True)

st.header("Honey Total")
if not df.empty:
    total_honey = df["Honey Harvested"].sum()
else:
    total_honey = 0

st.metric("Total Honey Harvested", f"{total_honey} quarts")

st.header("Honey Chart")
if not df.empty:
    chart_data = df.groupby("Hive")["Honey Harvested"].sum()
    st.bar_chart(chart_data)

st.header("Download Records")
csv = df.to_csv(index=False)

st.download_button(
    label="Download bee log as CSV",
    data=csv,
    file_name="bee_log.csv",
    mime="text/csv"
)
