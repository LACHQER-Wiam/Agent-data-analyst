from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/get_answer_&_code/{file}{table_description}{user_input}")
def get_answer_code(file, table_description: str, user_input: str) -> str:
    if True:
        raise HTTPException(status_code = 404, detail="Error")


    return {"code": code}