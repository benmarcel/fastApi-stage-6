from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, status
from model.user import UserRead, RegisterUser, LoginUser, RegisterAdmin
from db import get_session
from sqlmodel import Session
from services.auth_service import (
    register_user_service,
    authenticate_user_service,
    register_admin_service,
    reset_password_service,
    forgot_password_service,
)

user_router = APIRouter(prefix="/users", tags=["Users"])
admin_router = APIRouter(prefix="/admin", tags=["Admin"])
session_dependency = Annotated[Session, Depends(get_session)]


@user_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser, session: session_dependency):
    new_user, access_token = register_user_service(user, session)
    return UserRead(
        id=new_user.id, email=new_user.email, full_name=new_user.full_name,
        is_active=new_user.is_active, token=access_token,
    )


@user_router.post("/login", response_model=UserRead)
def login_user(user: LoginUser, session: session_dependency):
    existing_user, access_token = authenticate_user_service(user, session)
    return UserRead(
        id=existing_user.id, email=existing_user.email, full_name=existing_user.full_name,
        is_active=existing_user.is_active, token=access_token,
    )


@admin_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_admin(admin: RegisterAdmin, session: session_dependency):
    new_admin, access_token = register_admin_service(admin, session)
    return UserRead(
        id=new_admin.id, email=new_admin.email, full_name=new_admin.full_name,
        is_active=new_admin.is_active, token=access_token,
    )


@admin_router.post("/login", response_model=UserRead)
def login_admin(admin: LoginUser, session: session_dependency):
    existing_admin, access_token = authenticate_user_service(admin, session, admin_only=True)
    return UserRead(
        id=existing_admin.id, email=existing_admin.email, full_name=existing_admin.full_name,
        is_active=existing_admin.is_active, token=access_token,
    )

@user_router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(email: str, session: session_dependency, background_tasks: BackgroundTasks):
    forgot_password_service(email, session, background_tasks)
    return {"message": "If an account with that email exists, a password reset link has been sent."}

@user_router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(token: str, new_password: str, session: session_dependency):
    reset_password_service(token, new_password, session)
    # return {"message": "Password has been reset successfully.", "user_id": updated_user.id}
    return {"message": "Password has been reset successfully."}