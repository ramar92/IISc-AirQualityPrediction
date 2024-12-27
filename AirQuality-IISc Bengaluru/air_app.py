import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import GoogleGenerativeAI
import os

# Set Google API Key environment variable
google_api_key = "AIzaSyD86OJPAef4n27awKHhChvcuRh4oyC0LdE"

# Define a function to create agent
def create_agent(csv_file):
    agent = create_csv_agent(
        GoogleGenerativeAI(temperature=0, model="gemini-pro", google_api_key=google_api_key),
        csv_file,
        verbose=True,
        allow_dangerous_code=True  # Opt-in for this feature
    )
    return agent

# Streamlit UI setup
st.title("Data Insights with Large Language Model (LLM)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_data.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Create the agent for the uploaded CSV
    agent = create_agent("temp_data.csv")
    
    # Input question
    question = st.text_input("Ask a question about your data")
    
    if question:
        # Run the agent to get the answer
        try:
            answer = agent.run(question)
            st.write("Answer: ", answer)
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Optionally, display the uploaded data
    if st.checkbox("Show raw data"):
        import pandas as pd
        data = pd.read_csv("temp_data.csv")
        st.dataframe(data)

    # Clean up the temporary file
    os.remove("temp_data.csv")
