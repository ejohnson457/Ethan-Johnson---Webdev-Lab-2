import streamlit as st
import pandas as pd
import os

st.title("📋 Daily Wellness Survey")
st.write("Please answer the survey questions below to submit your daily statistics.")

# Define the local file path for storage
csv_path = "data.csv"

# Pre-defined questions to ensure clean mapping and structure
questions = {
    "Sleep Hours": "How much sleep do you get each night? (Enter numerical value or description)",
    "Mood Rating": "How would you rate your mood today? (Scale 1-10)",
    "Screen Time": "How many hours of screen time did you accumulate today?",
    "Exercise Log": "Did you perform any physical exercise today? (Yes/No/Details)"
}

# Collect user responses inside a clean submit form
with st.form(key="survey_form", clear_on_submit=True):
    user_responses = {}
    
    for metric, query_text in questions.items():
        # Captures responses strictly as strings per instructions
        user_responses[metric] = st.text_input(query_text, key=f"input_{metric}")
        
    submit_button = st.form_submit_button("Submit Entry")

if submit_button:
    # Validate that fields are not left entirely empty
    if any(value.strip() == "" for value in user_responses.values()):
        st.error("⚠️ All survey fields must be filled before submitting.")
    else:
        # Create a dictionary frame representing a single row
        new_row = {metric: [str(val).strip()] for metric, val in user_responses.items()}
        new_df = pd.DataFrame(new_row)
        
        # Append data frame to the data.csv storage layout safely
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            new_df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(csv_path, mode='w', header=True, index=False)
            
        st.success("✅ Your wellness entry was written to data.csv successfully!")
