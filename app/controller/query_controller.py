

from fastapi import APIRouter, HTTPException
from app.service.query_service import MyService
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryController:
    def __init__(self):
        self.router = APIRouter()
        self.service = MyService()

        @self.router.post("/query")
        def process_query(query_request: QueryRequest):
            try:
                result = self.service.query_vector_store(query_request.query)
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
