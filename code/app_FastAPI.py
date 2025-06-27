from fastapi import FastAPI, Path, HTTPException
from main import generate_answers
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/get_answer_code/{filename}/{table_description}/{user_input}/{analyzer}")
def get_answer_code(filename: str, table_description: str, user_input: str, analyzer: bool) -> dict:
    if 1==2:
        raise HTTPException(status_code = 404, detail="Error")
    
    code, answer, code_return = generate_answers(filename, 
                                                 user_input, 
                                                 table_description, 
                                                 analyzer=analyzer)
    
    if analyzer==False:
        code_return = code_return.to_dict(orient="records")

    return JSONResponse(content={"code": code,
            "answer": answer,
            "code_return": code_return})