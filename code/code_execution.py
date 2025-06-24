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
    cleaned += [
        "try:",
        "    if type(result)!=str:",
        "           result = list(result)",
        "except:",
        "    pass"
    ]

    return '\n'.join(cleaned)


###############
def cleaning_code_df(code_str):
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
    cleaned += [
        "pd.DataFrame(result).to_excel('results.xlsx')"
    ]

    return '\n'.join(cleaned)

################
def execute_code_safely(code, local_vars={}):

    # Step 2: Basic security check — forbid dangerous patterns
    forbidden_keywords = ['import os', 'os.system', 'subprocess', 'eval', 'exec', '__import__', 'open(', 'write(', 'delete', 'shutil']
    for keyword in forbidden_keywords:
        if keyword in code:
            return f"Security error: usage of '{keyword}' is not allowed."

    # Step 3: Try to execute
    try:
        exec(code, local_vars)
        return local_vars.get("result", "The variable 'result' is not defined.")
    except Exception as e:
        return f"Error during execution: {str(e)}"
