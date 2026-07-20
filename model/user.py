from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
if TYPE_CHECKING:
    from .product import Product
from pydantic import BaseModel, EmailStr

class UserBase(SQLModel):
    email: EmailStr
    full_name: str
    is_active: bool = True

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    products: list[Product] = Relationship(back_populates="admin")
    is_admin: bool = False

class RegisterUser(UserBase):
    password: str

class LoginUser(SQLModel):
    email: EmailStr
    password: str
class UserRead(UserBase):
    id: int | None = None
    token: str | None = None
class RegisterAdmin(UserBase):
    password: str
    is_admin: bool = True


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
