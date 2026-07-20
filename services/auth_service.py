from fastapi import BackgroundTasks, HTTPException, status
from sqlmodel import Session, select
from model.user import User, RegisterUser, LoginUser, RegisterAdmin
from middlewares.utilities import hash_password, verify_password, create_access_token, create_reset_token, verify_reset_token
from services.email_service import send_reset_email


def register_user_service(user: RegisterUser, session: Session) -> tuple[User, str]:
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    user_data = user.model_dump()
    user_data.pop("password")
    user_data["hashed_password"] = hash_password(user.password)

    new_user = User.model_validate(user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email, "user_id": new_user.id})
    return new_user, access_token


def authenticate_user_service(credentials: LoginUser, session: Session, admin_only: bool = False) -> tuple[User, str]:
    query = select(User).where(User.email == credentials.email)
    if admin_only:
        query = query.where(User.is_admin == True)

    existing_user = session.exec(query).first()
    if not existing_user or not verify_password(credentials.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(data={"sub": existing_user.email, "user_id": existing_user.id})
    return existing_user, access_token


def register_admin_service(admin: RegisterAdmin, session: Session) -> tuple[User, str]:
    existing_admin = session.exec(select(User).where(User.email == admin.email)).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists.",
        )

    admin_data = admin.model_dump()
    admin_data.pop("password")
    admin_data["hashed_password"] = hash_password(admin.password)
    admin_data["is_admin"] = True

    new_admin = User.model_validate(admin_data)
    session.add(new_admin)
    session.commit()
    session.refresh(new_admin)

    access_token = create_access_token(data={"sub": new_admin.email, "user_id": new_admin.id})
    return new_admin, access_token

    

def forgot_password_service(email: str, session: Session, background_tasks: BackgroundTasks) -> None:
    user = session.exec(select(User).where(User.email == email)).first()

    if user:
        reset_token = create_reset_token(data={"sub": user.email})
        background_tasks.add_task(send_reset_email, user.email, reset_token)


def reset_password_service(token: str, new_password: str, session: Session) -> User:
    payload = verify_reset_token(token)

    db_user = session.exec(select(User).where(User.email == payload["sub"])).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")

    db_user.hashed_password = hash_password(new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user