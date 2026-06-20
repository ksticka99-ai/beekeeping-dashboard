import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "bee_log.csv"

st.title("🐝 Beekeeping Dashboard")

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "Date", "Hive", "Queen Seen", "Brood Pattern",
        "Temperament", "Feed Added", "Honey Harvested",
        "Notes", "Next Action"
    ])

st.header("Add Hive Inspection")

with st.form("inspection_form"):
    hive = st.text_input("Hive name", "Main Hive")
    inspection_date = st.date_input("Inspection date", date.today())
    queen_seen = st.selectbox("Queen seen?", ["Yes", "No", "Not sure"])
    brood = st.text_input("Brood pattern", "Good")
    temperament = st.selectbox("Temperament", ["Calm", "Normal", "Spicy"])
    feed = st.text_input("Feed added", "None")
    honey = st.number_input("Honey harvested - quarts", min_value=0.0, step=0.25)
    notes = st.text_area("Notes")
    next_action = st.text_input("Next action")

    submitted = st.form_submit_button("Save Inspection")

    if submitted:
        new_row = {
            "Date": inspection_date,
            "Hive": hive,
            "Queen Seen": queen_seen,
            "Brood Pattern": brood,
            "Temperament": temperament,
            "Feed Added": feed,
            "Honey Harvested": honey,
            "Notes": notes,
            "Next Action": next_action
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Inspection saved!")

st.header("Hive Log")
st.dataframe(df)

st.header("Honey Total")
total_honey = df["Honey Harvested"].sum() if not df.empty else 0
st.metric("Total Honey Harvested", f"{total_honey} quarts")
