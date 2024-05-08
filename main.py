from fastapi import FastAPI
from app.controller import user_controller

app = FastAPI()

app.include_router(user_controller.router, prefix="/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
