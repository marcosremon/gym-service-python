from fastapi import FastAPI
from src.service.controller.user_controller import http as user_controller

app = FastAPI(debug=True)
app.include_router(user_controller)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=True)