import os
import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Any
def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise RuntimeError(f"{var_name} environment variable is not set.")
    return value
SECRET_KEY = get_env_variable("SECRET_KEY")
ALGORITHM = get_env_variable("ALGORITHM")
ACCESS_TOKEN_EXPIRE_IN = int(get_env_variable("ACCESS_TOKEN_EXPIRE_IN"))
RESET_TOKEN_EXPIRE_IN = int(get_env_variable("RESET_PASSWORD_TOKEN_EXPIRE_IN"))


# Replacement for pwd_context.hash()
def hash_password(password: str) -> str:
    # Convert the plain text password into raw bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a secure salt
    salt = bcrypt.gensalt(rounds=12)
    
    # Hash the password bytes using the salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Convert the resulting hashed bytes back to a standard string for DB storage
    return hashed_bytes.decode('utf-8')

# compare the plain password with the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert the user input to bytes
    plain_bytes = plain_password.encode('utf-8')
    
    # Convert the stored database hash back to bytes
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Securely compare them (prevents timing attacks)
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    payload: dict[str, Any] = data.copy()
    expires_in = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN)
    )
    payload["exp"] = expires_in
    access_token = jwt.encode(payload, str(SECRET_KEY), algorithm=ALGORITHM)
    return access_token

def verify_access_token(access_token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(access_token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")

def create_reset_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    payload: dict[str, Any] = data.copy()
    expires_in = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=RESET_TOKEN_EXPIRE_IN)
    )
    payload["exp"] = expires_in
    payload["purpose"] = "password_reset"
    reset_token = jwt.encode(payload, str(SECRET_KEY), algorithm=ALGORITHM)
    return reset_token

def verify_reset_token(reset_token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(reset_token, str(SECRET_KEY), algorithms=[ALGORITHM])
        if payload.get("purpose") != "password_reset":
            raise ValueError("Invalid token purpose")
        return payload
    except ExpiredSignatureError:
        raise ValueError("Reset token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid reset token")