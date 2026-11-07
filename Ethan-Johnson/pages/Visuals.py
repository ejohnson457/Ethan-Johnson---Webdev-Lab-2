import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("📊 Data Insights & Visualizations")

csv_path = "data.csv"

# 1. Graceful verification check if the data source exists and has data
if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    st.warning("⚠️ No survey data found in data.csv yet. Please submit data via the Survey page first.")
else:
    # Read the data file securely using pandas
    df = pd.read_csv(csv_path)
    
    # Clean whitespace from column names to avoid accidental mismatch errors
    df.columns = [col.strip() for col in df.columns]

    # 2. Dynamic Check: Ensure the required columns exist before processing
    required_columns = ["Sleep Hours", "Mood Rating", "Screen Time"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"⚠️ Your data.csv file is missing these expected columns: {missing_columns}")
        st.info("💡 **How to fix this:** Go to your **Survey** page and submit at least one response to properly create the file headers. Alternatively, delete your current `data.csv` file and let the survey page regenerate a fresh one.")
        
        # Display what columns DO exist to help you debug
        st.write("Columns currently found in your CSV:", list(df.columns))
        st.dataframe(df)
    else:
        # Standardize data to numeric conversions safely
        df_clean = df.copy()
        df_clean["Sleep Hours"] = pd.to_numeric(df_clean["Sleep Hours"], errors='coerce').fillna(0)
        df_clean["Mood Rating"] = pd.to_numeric(df_clean["Mood Rating"], errors='coerce').fillna(5)
        df_clean["Screen Time"] = pd.to_numeric(df_clean["Screen Time"], errors='coerce').fillna(0)

        st.subheader("Raw Submission History Table")
        st.dataframe(df)

        st.divider()

        # ----------------------------------------------------
        # VISUALIZATION 1: Static Chart (Pie Chart Distribution)
        # ----------------------------------------------------
        st.subheader("1. Mood Distribution Breakdown (Static)")
        st.write("This chart is static; its presentation matrix depends entirely on your historical CSV records.")
        
        mood_counts = df_clean["Mood Rating"].value_counts().sort_index()
        
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.pie(mood_counts, labels=[f"Rating: {int(i)}" for i in mood_counts.index], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        ax1.axis('equal')  
        plt.title("Proportion of Historical Daily Mood Ratings")
        
        st.pyplot(fig1)

        st.divider()

        # ----------------------------------------------------
        # VISUALIZATION 2: Dynamic & Advanced Chart (Scatter / Line Plot)
        # ----------------------------------------------------
        st.subheader("2. Wellness Variable Correlation (Dynamic & Advanced)")
        st.write("This interactive section changes dynamically via user widget inputs without refreshing your global data structures.")

        # State controller initialization tracking user interactive variables
        if "x_metric" not in st.session_state:
            st.session_state.x_metric = "Sleep Hours"
        if "chart_color" not in st.session_state:
            st.session_state.chart_color = "Deep Sky Blue"

        # Interactive Widget controls matching dynamic spec rules
        available_metrics = ["Sleep Hours", "Mood Rating", "Screen Time"]
        color_map = {"Deep Sky Blue": "#00BFFF", "Crimson": "#DC143C", "Emerald Green": "#50C878", "Vibrant Purple": "#9B59B6"}

        col1, col2 = st.columns(2)
        with col1:
            selected_x = st.selectbox(
                "Select X-Axis Data Component:", 
                options=available_metrics, 
                index=available_metrics.index(st.session_state.x_metric)
            )
            st.session_state.x_metric = selected_x
            
        with col2:
            selected_color = st.selectbox(
                "Select Visualization Color Theme:", 
                options=list(color_map.keys()), 
                index=list(color_map.keys()).index(st.session_state.chart_color)
            )
            st.session_state.chart_color = selected_color

        # Building the dynamic Advanced Plot using Matplotlib
        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        
        # Sort data by selection choice sequence pathing
        df_sorted = df_clean.sort_values(by=st.session_state.x_metric)
        
        ax2.plot(
            df_sorted[st.session_state.x_metric], 
            df_sorted["Mood Rating"], 
            marker='o', 
            linestyle='-', 
            color=color_map[st.session_state.chart_color], 
            linewidth=2, 
            markersize=8,
            label="Mood Trend Tracker"
        )
        
        ax2.set_title(f"Dynamic Assessment: Impact of {st.session_state.x_metric} on Mood Rating", fontsize=12, fontweight='bold')
        ax2.set_xlabel(st.session_state.x_metric, fontsize=10)
        ax2.set_ylabel("Mood Rating (1-10 Scale)", fontsize=10)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.legend()

        st.pyplot(fig2)
