from modules import *
from langchain_ollama import OllamaLLM


def generate_answers(filename, user_input, table_description, analyzer=True):

    llm_reasoning_formulation = OllamaLLM(
    model="gemma:2b",              # "deepseek-coder:1.3b"
    temperature=0.2,
    top_k=10,                 
    repeat_penalty=1.1,       
    seed=42
    )

    llm_coding =  OllamaLLM(
        model="phi",
        temperature=0.2,
        top_k=10,              
        repeat_penalty=1.1,      
        seed=42
    )


    # Initiate a memory object
    memory = Memory()

    # Reasoning step
    reasoner = Reasoner(llm=llm_reasoning_formulation, 
                user_input=user_input, 
                table_description=table_description, 
                context=memory.list_messages)

    reasoning = reasoner.process_question(filename=filename)

    # Programming step 
    programmer = Programmer(llm=llm_coding, 
                            user_input=user_input, 
                            table_description=table_description, 
                            reasoning=reasoning, 
                            analyzer=analyzer)
    
    clean_code = programmer.process_question(filename=filename)

    # Execute the code
    code_return = Programmer.execute_code_safely(clean_code)
    
    # Formulation step 
    if analyzer==True:
        formulator = Formulator(llm=llm_reasoning_formulation,
                                user_input=user_input, 
                                code_return=code_return)
        
        answer = formulator.process_question()
    
    else:
        answer = ("An Excel file is downloaded in the folder 'data' ")


    return clean_code, answer 

