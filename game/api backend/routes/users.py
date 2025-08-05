from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    # TODO: Implement user creation
    return UserOut(username=user.username)

@router.post("/login")
def login():
    # TODO: Implement login
    return {"token": "jwt_token"}
