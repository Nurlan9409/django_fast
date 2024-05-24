from fastapi import APIRouter

model_router = APIRouter(prefix="/models")

@model_router.get("/")
async def get_models():
    return {
        "message": "Model page"
    }
@model_router.post("/model")
async def model_1():
    return {
        "message": "Model page1"
    }

