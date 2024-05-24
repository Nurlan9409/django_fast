from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")

@auth_router.get("/")
async def auth():
    return{
        "messege":"this is an auth page",
    }

@auth_router.get("/login")
async def login():
    return{
        "messege":"this is an login page",
    }

@auth_router.get("/register")
async def register():
    return{
        "messege":"this is an register page",
    }

