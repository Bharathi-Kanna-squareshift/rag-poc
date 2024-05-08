from fastapi import FastAPI
from app.controller import QueryController

app = FastAPI()

query_controller = QueryController()
app.include_router(query_controller.router, prefix="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)