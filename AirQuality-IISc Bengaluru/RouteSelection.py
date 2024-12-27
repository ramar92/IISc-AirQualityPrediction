import pandas as pd
import numpy as np
import streamlit as st

# Title of the web app
st.title("Air Quality Assessment and Best Route Selection")

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded data
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.write("Dataset Preview:")
    st.write(df.head())

    # Define ideal ranges
    IDEAL_PM2_5 = 25  # Safe limit for PM2.5 in µg/m³
    IDEAL_PM10 = 50   # Safe limit for PM10 in µg/m³
    IDEAL_TEMP_RANGE = (20, 25)  # Ideal temperature range in °C
    IDEAL_HUMIDITY_RANGE = (40, 60)  # Ideal humidity range in %

    # Calculate scores for each row
    def calculate_score(row):
        # PM2.5 and PM10: The lower, the better
        pm2_5_score = max(0, 1 - (row['PM2.5 (ug/m3)'] / IDEAL_PM2_5))
        pm10_score = max(0, 1 - (row['PM10 (ug/m3)'] / IDEAL_PM10))

        # Temperature: Score based on deviation from ideal range
        temp_score = 1 if IDEAL_TEMP_RANGE[0] <= row['Temperature (C)'] <= IDEAL_TEMP_RANGE[1] else 0

        # Humidity: Score based on deviation from ideal range
        humidity_score = 1 if IDEAL_HUMIDITY_RANGE[0] <= row['Humidity (%)'] <= IDEAL_HUMIDITY_RANGE[1] else 0

        # Combine scores
        return pm2_5_score + pm10_score + temp_score + humidity_score

    # Apply scoring
    df['Score'] = df.apply(calculate_score, axis=1)

    # Group by Route and calculate average scores
    route_scores = df.groupby('Route')['Score'].mean().reset_index()

    # Find the best route
    best_route = route_scores.sort_values(by='Score', ascending=False).iloc[0]
    # Find the note best route
    notbe_route = route_scores.sort_values(by='Score', ascending=True).iloc[0]


    # Display the result
    st.write(f"The best route is **{best_route['Route']}** with an average score of **{best_route['Score']:.2f}**")
    # Display the result
    st.write(f"The Not best route is **{notbe_route['Route']}** with an average score of **{notbe_route['Score']:.2f}**")

    # Optionally, display route scores
    st.write("Route Scores Overview:")
    st.write(route_scores)
