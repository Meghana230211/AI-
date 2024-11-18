import os
import base64
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for APIs
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to convert an image to base64
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error reading image: {str(e)}")
        return None

# Path to the local image (adjust the path as needed)
image_path = "image.jpg"  # Replace with your actual image path

# Convert image to base64
base64_image = image_to_base64(image_path)

# Check if the image is being read and encoded correctly
if base64_image:
    st.write(f" ")  # Debugging step to check the length of the base64 string
else:
    st.stop()  # Stop execution if the image isn't loading

# Add background image via CSS if base64 encoding is successful
st.markdown(
    f"""
    <style>
        body {{
            background-image: url('data:image/jpeg;base64,{base64_image}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        .stApp {{
            background-color: transparent;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit Dashboard
st.title("AI search agent")
st.write("Upload your dataset and extract multiple fields dynamically.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.dataframe(df.head())

    # Select column for queries
    column = st.selectbox("Select the column to query", df.columns)

    # Input multiple-field prompt
    user_prompt = st.text_area("Enter your prompt (e.g., Get the email and phone of {entity}):")
    if st.button("Process Data"):
        st.write("Processing...")
        results = []

        # Iterate over entities in the selected column
        for entity in df[column]:
            query = user_prompt.replace("{entity}", entity)
            # Use your search and GPT function here
            results.append({"Entity": entity, "Extracted Data": "Data"})  # Example result

        # Display results
        result_df = pd.DataFrame(results)
        st.write("Extraction Results:")
        st.dataframe(result_df)

        # Download results as CSV
        st.download_button(
            label="Download Results as CSV",
            data=result_df.to_csv(index=False),
            file_name="extracted_results.csv",
            mime="text/csv"
        )
