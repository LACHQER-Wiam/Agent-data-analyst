from langchain_ollama import OllamaLLM
import pandas as pd
import textwrap
import json
from memory import  concatenate_messages, concatenate_code_input
from code_execution import execute_code_safely, cleaning_code, cleaning_code_df
from transformers import AutoTokenizer



llm = OllamaLLM(
    model="gemma:2b",              # "deepseek-coder:1.3b"
    temperature=0.2,
    top_k=10,                 # restricts to the 10 most probable tokens
    repeat_penalty=1.1,       # prevents the model from repeating the same things
    #stop=["```"],            # stops generation when one of these strings is encountered
    #num_predict=100,         # limits the number of generated tokens
    seed=42
)

llm_code =  OllamaLLM(
    model="phi",
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

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")


context = []
context_code = []

def process_questions(filename, 
                      user_input, 
                      table_description, 
                      context=context,
                      context_code=context_code,
                      llm=llm, 
                      llm_code=llm_code, 
                      llm_reformulation=llm_reformulation,
                      generate_dataframe=False) : 
    

    path = f"../data/{filename}"

    if filename.endswith(".xlsx"):
        file_extension = "excel"
    elif filename.endswith(".csv"):
        file_extension = "csv"

    reasoning_prompt = f'''You are a concise Python assistant.

            Your task is not to write Python code, but to think step by step and explain how to answer the user's 
            question using the Pandas DataFrame named {path}.

            The first step must be : reading the file pd.read_{file_extension}({path})

            Here is a description of the DataFrame:
            {table_description}

            Here is the user's question:
            {user_input}

            Use the previous messages as context if needed:
            {context}

            Instructions:
            Do not generate any Python code.

            Provide only the essential reasoning steps, using bullets or numbers.

            Be brief, clear, and focused — no unnecessary operations.

            Do not mention imports or packages.

            Each step should describe one concise DataFrame operation (e.g., filter, group, aggregate).

            Skip any step that is not strictly required to answer the question.

            You must always assign the dataframe to a variable named df , and the final answer to a variable named `result`, that is important
 
            If the user asks for a dataframe as an output, the variable 'result' must contain a pd.DataFrame
    '''

    reasoning = llm.invoke(reasoning_prompt)
    print(reasoning)

    ####### Code generation and execution

    code_prompt = f""" You are a Python assistant, you must implement the reasoning steps in python.

        Your task is to write valid Python code that answers the user's question using the Pandas DataFrame named `{path}`  
        Follow these steps and implement them in one python block: {reasoning}

        Here is a description of the DataFrame:
        {table_description}

        Here is the user's question:
        {user_input}

        You must always assign your answer to a variable named `result`, 
        it must contain a number, or a string, or a list of numbers or a list of strings.
        
        do not print the result
        Only output the Python code.
        Do not explain the code.
        DO NOT output the instructions
        Use datatimes as they are given to you in the instructions, do not change them
        """

    code = llm_code.invoke(code_prompt)

    if generate_dataframe==True:
        clean_code = cleaning_code_df(code) 
    else:
        clean_code = cleaning_code(code) 
    
    code_return = execute_code_safely(code=clean_code)


    ###### Return a coherent answer

    prompt_reformulation = f'''
        You are a language assistant.

        Your task is to take a user question and answer (already calculated), it can be a number or a list of words, 
        and generate a natural, well-structured sentence that communicates the answer clearly.

        Return only the sentence that I request, without the introductory sentence : "Sure, here is the sentence you requested:"

        Do not try to calculate or infer the result yourself — just rephrase it into a readable sentence.

        Question: "{user_input}"
        Answer: "{code_return}"

        Write a clear and concise sentence using both.

    '''

    # Examples (do not copy, get inspiration):
    #     Example 1:
    #     Question: "What is the average quantity sold?"

    #     Answer: "XXX"

    #     → Output :
    #     "The average quantity sold is XXX."

    #     Example 2: 
    #     Question: What the list of values in the column1 ?
    #     Answer: ["Element1","Element2","Element3","Element4"]

    #     → Output :
    #     "The list of values in the column1 is ["Element1","Element2","Element3","Element4"] "
    
    answer = llm_reformulation.invoke(prompt_reformulation)


    # # ####### Memory
    context = concatenate_messages(user_input, answer, context)

    context_code = concatenate_code_input(user_input, clean_code, context_code)


    return clean_code, answer 