import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from io import StringIO

# Title of the web app
st.title("Air Quality Data with PM2.5 and PM10")

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded data
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.write("Dataset Preview:")
    st.write(df.head())

    # Check if required columns exist
    if 'Latitude' in df.columns and 'Longitude' in df.columns and 'PM2.5 (ug/m3)' in df.columns and 'PM10 (ug/m3)' in df.columns:
        # Create a map centered around a location (use the average lat/lon for centering)
        map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)

        # Marker cluster to group close markers together
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers for each row in the dataset
        for index, row in df.iterrows():
            lat, lon = row['Latitude'], row['Longitude']
            pm2_5 = row['PM2.5 (ug/m3)']
            pm10 = row['PM10 (ug/m3)']
            
            # Add a marker with a popup displaying the PM values
            popup = f"PM2.5: {pm2_5} µg/m³<br>PM10: {pm10} µg/m³"
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                icon=folium.Icon(color='blue')
            ).add_to(marker_cluster)

        # Display the map
      
