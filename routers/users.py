from fastapi import APIRouter, status, HTTPException, Form
from pydantic import BaseModel
from typing import Annotated
from services.user_service import read_logged_users, logout

#Define user models for creation and logging in
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    email: str    

router = APIRouter()

@router.put("/log-out", status_code=status.HTTP_200_OK)
async def log_out(username: Annotated[str, Form()]):
    users = read_logged_users()
    for user in users:
        if user == username:
            logout(user)
            return {f'message: {username} logged out'}
    raise HTTPException(status_code=404, detail=f"User {username} is not logged in.")
            
    

