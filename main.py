# main.py
from fastapi import FastAPI, HTTPException
from query import run_query

app = FastAPI()

@app.post("/process-query")
def process_query(query: str):
    try:
        result = run_query(query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
