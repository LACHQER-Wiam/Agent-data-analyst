from langchain_ollama import OllamaLLM
import pandas as pd
import textwrap
import json
from memory import summarize
from code_execution import execute_code_safely

llm = OllamaLLM(
    model="phi",              # "deepseek-coder:1.3b"
    temperature=0.2,
    top_k=10,                 # restricts to the 10 most probable tokens
    repeat_penalty=1.1,       # prevents the model from repeating the same things
    #stop=["```"],            # stops generation when one of these strings is encountered
    #num_predict=100,         # limits the number of generated tokens
    seed=42
)

llm_summary = OllamaLLM(model="gemma:2b", 
                temperature=0)



def process_questions(filename, user_input, table_description, llm=llm) : 
    path = f"../data/{filename}"
    # if user_input.lower() in ['exit', 'quit']:
    #     break

    final_prompt = f""" You are a Python assistant.

        Your task is to write valid Python code that answers the user's question using the Pandas DataFrame named `{path}`.

        Here is a description of the DataFrame:
        {table_description}

        Here is the user's question:
        {user_input}

        You must always assign your answer to a variable named `result`, it must contain a number, not a string.

        Only output the Python code.
        Do not explain the code.
        DO NOT output the instructions
        Print <END> in the end of Python code
        """

    response = llm.invoke(final_prompt)
    
    answer = execute_code_safely(code=response)

    return answer 