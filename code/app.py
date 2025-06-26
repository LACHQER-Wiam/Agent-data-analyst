import streamlit as st
import pandas as pd
from main import generate_answers


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
        filename = uploaded_file.name.lower()
        
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(".xlsx"):
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

col_analyze, col_download = st.columns(2)

if df is not None and user_input:

    # Bouton Analyze (sans fichier à télécharger)
    if col_analyze.button("Analyze"):
        question = user_input
        with st.spinner("🤖 Processing..."):
            try:
                code, answer = generate_answers(filename, user_input, table_description, analyzer=True)
            except Exception as e:
                code = ""
                answer = f"💥 Error while analyzing: {e}"

        st.session_state.chat_history.append((question, answer, code))

        st.markdown(f"**🧑 You:** {question}")
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown("**📊 Answer:**")
            st.success(answer)
        with col2:
            st.markdown("**💻 Python Code:**")
            st.code(code, language="python")



    if col_download.button("Download Excel File"):
        question = user_input
        with st.spinner("🤖 Processing..."):
            try:
                code, answer = generate_answers(filename, user_input, table_description, analyzer=False)
            except Exception as e:
                code = ""
                answer = f"💥 Error while analyzing: {e}"

        st.session_state.chat_history.append((question, answer, code))

        st.markdown(f"**🧑 You:** {question}")
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown("**📊 Answer:**")
            st.success(answer)
        with col2:
            st.markdown("**💻 Python Code:**")
            st.code(code, language="python")

    # # Bouton Download (avec DataFrame généré)

    #     st.session_state.chat_history.append((question, answer, code))

    #     st.markdown(f"**🧑 You:** {question}")
    #     col1, col2 = st.columns([2, 3])
    #     with col1:
    #         st.markdown("**📊 Answer:**")
    #         st.success(answer)
    #     with col2:
    #         st.markdown("**💻 Python Code:**")
    #         st.code(code, language="python")
