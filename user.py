from fastapi import APIRouter
from database import session, ENGINE
from schemas import UserModel
from models import User
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = session(bind=ENGINE)

user_router = APIRouter(prefix="/user")


@user_router.get("/")
async def get(status_code=status.HTTP_200_OK):
    user= session.query(User).all()
    context = [
        {
            "id": users.id,
            "username": users.username,
        }
        for users in user
    ]

    return jsonable_encoder(context)


@user_router.post("/create")
async def create(user: UserModel):
    check_user = session.query(User).filter(User.id == user.id).first()
    if check_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allready exists")

    new_user = User(
        id=user.id,
        first_name=user.firstname,
        last_name=user.lastname,
        username=user.username,
        password=user.password,
        is_staff=user.is_staff,
        is_active=user.is_active,

    )
    session.add(new_user)
    session.commit()

    return user



@user_router.delete("/delete")
async def delete(user: UserModel):
    check_user = session.query(User).filter(User.id == user.id).first()
    if check_user:
        session.delete(check_user)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



