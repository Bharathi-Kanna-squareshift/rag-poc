from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service import MyService

from app.controller import QueryRequest

router = APIRouter()


my_service = MyService()

@router.post("/query")
def process_query(query_request: QueryRequest):
    try:
        result = my_service.query_vector_store(query_request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
