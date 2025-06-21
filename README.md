# 🤖 DataBot — Your Data Analyst Assistant

## 📌 Project Overview

**DataBot** is a lightweight AI assistant designed to analyze Excel or CSV tables and answer natural language questions about the data.

Its key strength lies in its ability to:
- Understand user questions written in plain English
- Generate the **exact Python code** (using pandas) to answer the question
- Execute the code and return the **numerical result**
- Display both the **answer** and the **code used**, side-by-side in a clean interface

Whether you're a data beginner or analyst, DataBot helps you query your data without writing code.

---

## ⚙️ Tech Stack

The assistant is built with the following components:

### 🧠 Small LLMs via Ollama
- **Phi-2** (Microsoft): for reasoning and Python code generation (very lightweight)
- **Gemma:2B** (Google): used to rephrase the final answer into a clear, human-readable sentence

Phi-2 receives the question and generates the corresponding Python code → the code is executed automatically in Python → Gemma:2B receives both the original question and the code output, and returns a clear, human-readable sentence.

### 🖥 Interface
- **Streamlit**: used to build a clean, fast, and user-friendly web interface

---

## 🛠 Features

✅ Upload Excel or CSV files  
✅ Ask data questions  
✅ Automatically generate Python code  
✅ Display both:
- the **executed code**
- the **final numerical answer** (rephrased for humans)

---

## 🚧 Coming Soon

- 🧠 **Memory system** for multi-turn conversations
- 📊 **Automatic chart generation** (bar plots, line charts, etc.)
- 📥 **Export features**: download the extracted tables 

---

## ▶️ Getting Started

Clone the repo and run:

```bash
pip install -r requirements.txt
streamlit run app.py```

Make sure you have Ollama installed locally and the required models pulled:
```bash
ollama pull phi
ollama pull gemma:2b```

📂 Project Structure
├── code
    ├── app.py                          # Streamlit frontend
    ├── function_numbers_generator.py   # Main agent logic
    ├── code_execution.py               # Functions that are used to clean the code and execute it
    ├── memory.py                       # Functions that are used to manage the memory
├── data                                # It contains synthetic datasets for testing
