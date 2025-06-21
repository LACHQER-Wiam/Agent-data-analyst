import streamlit as st
import pandas as pd
from function_numbers_generator import process_questions  # adapt to your own module

st.set_page_config(page_title="DataBot", 
                   layout="centered")

st.title("📊 Data Assistant")
st.markdown("Ask a natural language question about your file 📈")

# Upload the file (CSV or Excel)
uploaded_file = st.file_uploader("Upload a file (.xlsx or .csv)", type=["xlsx", "csv"])

df = None

if uploaded_file:
    try:
        # Get file extension
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("Unsupported file type. Please upload a .csv or .xlsx file.")
        
        if df is not None:
            st.success("✅ File successfully loaded!")
            st.write("Preview of the table:")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error while loading the file: {e}")

# User input
user_input = st.text_input("Hello, what is your question?")
# Filename
filename = st.text_input("Hello, what is your filename")
# Table's description
table_description = st.text_input("Hello, describe briefly your table, provide correct columns' names")

# Analyze button
if st.button("Analyze") and df is not None and user_input:
    with st.spinner("🤖 Processing..."):
        try:
            result = process_questions(filename, user_input, table_description)
            st.success("✅ Answer:")
            st.write(result)
        except Exception as e:
            st.error(f"Error while analyzing: {e}")