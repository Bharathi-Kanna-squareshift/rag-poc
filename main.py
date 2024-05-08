# main.py
from fastapi import FastAPI, HTTPException
from query import run_query

app = FastAPI()

@app.post("/process-query")
def process_query(query_request: dict):
    query = query_request.get("query")
    if not query:
        raise HTTPException(status_code=422, detail="Query parameter is missing")
    
    try:
        result = run_query(query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}