import pandas as pd


def summarize(llm_summary, last_exchange, old_summaries):
    prompt = f"""You are a highly qualified assistant responsible of finding relevant information in a discussion. 
    You will recieve a discussion between a user and an AI assistant
    Return 4 or less sentences containing the most important information.
    You must distinguish between the user and the assistant, they are two different people
    Return the most important information like personal information, statistics, emotions , do not retain irrelevant information like hello
    DO NOT Include additional information
    DO NOT ANSWER THE QUESTIONS, your role is to analyze the discussion, do not intervene

    The output :
    4 sentences or less that contain relevant information from old messages
    
    Here is the discussion:
    *** Discussion :
    {old_summaries}{last_exchange}

    """
    response = llm_summary.invoke(prompt)
    
    print(f"Summary : {response}")
    return response



