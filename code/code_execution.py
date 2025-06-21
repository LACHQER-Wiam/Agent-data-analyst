import pandas as pd
import textwrap
import json
import re

###############
def cleaning_code(code_str):
    '''Cleaning the generated code'''
    # Step 0: Remove everything after the word "Rules"
    if "Rules" in code_str:
        code_str = code_str.split("Rules", 1)[0]

    # Step 1: Dedent the code
    code_str = textwrap.dedent(code_str)

    # Step 2: Clean line by line
    lines = code_str.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.lstrip()
        # Remove lines starting with "print" or "```", case-insensitive for "print"
        if not stripped.lower().startswith("print") and not stripped.startswith("```"):
            cleaned.append(stripped)

    return '\n'.join(cleaned)

################
def execute_code_safely(code, local_vars={}):

    # Step 1: Clean the code
    clean_code = cleaning_code(code)
    print(clean_code)

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
