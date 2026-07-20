from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from datetime import datetime, timezone
if TYPE_CHECKING:
    from .user import User
from sqlalchemy.dialects.postgresql import ARRAY
#1. Product ID (integer)

#2. Product name (string)

#3. Product description (string)

#4 Product cost (float)

#5. Product picture (an array of strings)

#6. Created At (Date)

#7. Updated At(Date)
class ProductBase(SQLModel):
    name: str
    description: str
    cost: float
    pictures: list[str] = Field(default=[], sa_column=Column(ARRAY(String))) #This means the list will be saved directly into a native text[] column in Postgres, rather than being serialized into text or a JSON block.

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    admin: User = Relationship(back_populates="products")
    admin_id: int  = Field(default=None, foreign_key="user.id")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    cost: float | None = None
    pictures: list[str] | None = None
