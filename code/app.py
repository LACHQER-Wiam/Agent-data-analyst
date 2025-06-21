import streamlit as st
import pandas as pd
from function_numbers_generator import process_questions  # adapt to your own module
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Retrieve the root
ROOT_DIR = os.getenv("ROOT_DIR")


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


# Table's description
table_description = st.text_input("Hello, describe briefly your table, provide correct columns' names")


# --- Initialisation de l'historique ---
if "chat_history" not in st.session_state:
    # Chaque entrée : (question, réponse, code)
    st.session_state.chat_history = []

# --- Affichage de l'historique avec deux colonnes ---
for question, answer, code in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {question}")
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("**📊 Answer:**")
        st.success(answer)
    with col2:
        st.markdown("**💻 Python Code:**")
        st.code(code, language="python")

# --- Input utilisateur ---
st.markdown("---")
user_input = st.text_input("💬 Your question:", key="user_input")

if st.button("Analyze") and df is not None and st.session_state.user_input:
    question = st.session_state.user_input

    with st.spinner("🤖 Processing..."):
        try:
            code, answer = process_questions(file_name, question, table_description)
        except Exception as e:
            code = ""
            answer = f"💥 Error while analyzing: {e}"

    # Ajouter à l'historique
    st.session_state.chat_history.append((question, answer, code))

    st.markdown(f"**🧑 You:** {question}")
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("**📊 Answer:**")
        st.success(answer)
    with col2:
        st.markdown("**💻 Python Code:**")
        st.code(code, language="python")
