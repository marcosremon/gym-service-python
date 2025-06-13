from fastapi import FastAPI
from src.service.controller.user_controller import http as user_controller

app = FastAPI()

app.include_router(user_controller)