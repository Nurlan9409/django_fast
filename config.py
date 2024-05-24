from fastapi import  FastAPI
from auth import auth_router
from models import model_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(model_router)

"""app.include_router(models.router)"""
@app.get("/")
async def intro():
    return {
        "meseege": "Welcome to my fast api"
    }

@app.get("/config")
async def user():
    return {
        "messege": "Welcome to gonfig user api"
    }