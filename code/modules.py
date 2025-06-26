import pandas as pd
import textwrap
import json
import abc
from typing import Union, List


##################
class BaseClass(abc.ABC):
    def __init__(self, llm, user_input: str):
        self.user_input = user_input
        self.llm = llm
    
    @abc.abstractmethod
    def process_question(self):
        raise NotImplementedError("method not implemented")
    

###################
class Reasoner(BaseClass):
    def __init__(self, llm, user_input: str, table_description: str, context:str):
        super().__init__(llm, user_input)
        self.table_description = table_description
        self.context = context

    def process_question(self, filename:str) -> str :

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
                {self.table_description}

                Here is the user's question:
                {self.user_input}

                Use the previous messages as context if needed:
                {self.context}

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

        reasoning = self.llm.invoke(reasoning_prompt)

        return reasoning

###################
class Programmer(BaseClass):
    def __init__(self, llm, user_input: str, table_description: str, reasoning: str, analyzer: bool):
        super().__init__(llm, user_input)
        self.table_description = table_description
        self.reasoning = reasoning
        self.analyzer = analyzer
    

    def process_question(self, filename:str) -> str :

        path = f"../data/{filename}"
        
        code_prompt = f""" You are a Python assistant, you must implement the reasoning steps in python.

        Your task is to write valid Python code that answers the user's question using the Pandas DataFrame named `{path}`  
        Follow these steps and implement them in one python block: {self.reasoning}

        Here is a description of the DataFrame:
        {self.table_description}

        Here is the user's question:
        {self.user_input}

        You must always assign your answer to a variable named `result`, 
        it must contain a number, or a string, or a list of numbers or a list of strings.
        
        do not print the result
        Only output the Python code.
        Do not explain the code.
        DO NOT output the instructions
        Use datatimes as they are given to you in the instructions, do not change them
        """
        generated_code = self.llm.invoke(code_prompt)

        clean_code = self.cleaning_code(generated_code) 
        
        return clean_code

    def cleaning_code(self, code_str: str) -> str :
        '''Cleaning the generated code'''

        # Step 0: Remove everything after the word "Rules"
        if "Rules" in code_str:
            code_str = code_str.split("Rules", 1)[0]

        # Step 1: Dedent the code
        code_str = textwrap.dedent(code_str)

        # Step 2: Split into lines and skip everything before the first "import"
        lines = code_str.splitlines()
        start_index = 0
        for i, line in enumerate(lines):
            if "import" in line:
                start_index = i
                break

        lines = lines[start_index:]

        # Step 3: Keep lines until (and including) the one starting with "result ="
        cleaned = []
        for line in lines:
            stripped = line.lstrip()
            cleaned.append(stripped)
            if stripped.startswith("result ="):
                break

        # Step 4: Remove unwanted lines
        cleaned = [
            line for line in cleaned
            if not line.lower().startswith("print") and not line.startswith("```")
        ]

        # Step 5 : add some steps 
        if self.analyzer==True :
            cleaned += [
                "try:",
                "    if type(result)!=str:",
                "           result = list(result)",
                "except:",
                "    pass"
            ]
        else:
            cleaned += [
                "pd.DataFrame(result).to_excel('../data/results.xlsx')"
            ]

        return '\n'.join(cleaned)
    

    @ staticmethod
    def execute_code_safely(clean_code, local_vars={}):
        # Step 2: Basic security check — forbid dangerous patterns
        forbidden_keywords = ['import os', 'os.system', 'subprocess', 'eval', 'exec', '__import__', 'open(', 'write(', 'delete', 'shutil']
        for keyword in forbidden_keywords:
            if keyword in clean_code:
                return f"Security error: usage of '{keyword}' is not allowed."

        # Step 3: Try to execute
        try:
            exec(clean_code, local_vars)
            return local_vars.get("result", "The variable 'result' is not defined.")
        except Exception as e:
            return f"Error during execution: {str(e)}"

###################
class Formulator(BaseClass):
    def __init__(self, llm, user_input: str, code_return: Union[float, int, List[Union[float, int, str]]]):
        super().__init__(llm, user_input)
        self.code_return = code_return

    def process_question(self):
        prompt_formulation = f'''
        You are a language assistant.

        Your task is to take a user question and answer (already calculated), it can be a number or a list of words, 
        and generate a natural, well-structured sentence that communicates the answer clearly.

        Return only the sentence that I request, without the introductory sentence : "Sure, here is the sentence you requested:"

        Do not try to calculate or infer the result yourself — just rephrase it into a readable sentence.

        Question: "{self.user_input}"
        Answer: "{self.code_return}"

        Write a clear and concise sentence using both.
        '''
        answer = self.llm.invoke(prompt_formulation)
        
        return answer
    
###################
class Memory():
    def __init__(self):
        self.list_messages = []

    def update(self, user_input: str, answer: str):
        dict_messages = {"User":user_input, "You":answer}
        self.list_messages.append(dict_messages)
        if len(self.list_messages)>3:
            self.list_messages = self.list_messages[1:]

