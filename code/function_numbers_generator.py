from langchain_ollama import OllamaLLM
import pandas as pd
import textwrap
import json
from memory import summarize
from code_execution import execute_code_safely, cleaning_code

llm = OllamaLLM(
    model="phi",              # "deepseek-coder:1.3b"
    temperature=0.2,
    top_k=10,                 # restricts to the 10 most probable tokens
    repeat_penalty=1.1,       # prevents the model from repeating the same things
    #stop=["```"],            # stops generation when one of these strings is encountered
    #num_predict=100,         # limits the number of generated tokens
    seed=42
)

llm_reformulation = OllamaLLM(model="gemma:2b", 
                temperature=0)

llm_summary = OllamaLLM(model="gemma:2b", 
                temperature=0)



def process_questions(filename, 
                      user_input, 
                      table_description, 
                      llm=llm, 
                      llm_reformulation=llm_reformulation) : 
    

    path = f"../data/{filename}"

    final_prompt = f""" You are a Python assistant.

        Your task is to write valid Python code that answers the user's question using the Pandas DataFrame named `{path}`.

        Here is a description of the DataFrame:
        {table_description}

        Here is the user's question:
        {user_input}

        You must always assign your answer to a variable named `result`, it must contain a number, or a string, or a list of numbers or a list of strings.

        Only output the Python code.
        Do not explain the code.
        DO NOT output the instructions
        """

    code = llm.invoke(final_prompt)

    clean_code = cleaning_code(code)
    
    code_return = execute_code_safely(code=clean_code)

    ### Return a coherent answer

    prompt_reformulation = f'''
        You are a language assistant.

        Your task is to take a user question and answer (already calculated), it can be a number or a list of words, 
        and generate a natural, well-structured sentence that communicates the answer clearly.

        Return only the sentence that I request, without the introductory sentence : "Sure, here is the sentence you requested:"

        Do not try to calculate or infer the result yourself — just rephrase it into a readable sentence.

        Question: "{user_input}"
        Answer: "{code_return}"

        Write a clear and concise sentence using both.

        Example (do not copy, get inspiration):
        Question: "What is the average quantity sold?"

        Answer: "57.2"

        → Output :
        "The average quantity sold is 57.2."
    '''

    answer = llm_reformulation.invoke(prompt_reformulation)


    return clean_code, answer 