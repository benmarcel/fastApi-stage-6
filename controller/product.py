from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from db import get_session
from middlewares.dependencies import get_current_admin
from model.user import User
from model.product import ProductCreate, ProductRead, ProductUpdate
from services.product_service import (
    get_products_service,
    get_product_by_id_service,
    create_product_service,
    update_product_service,
    delete_product_service,
)

router = APIRouter(prefix="/products", tags=["Products"])
session_dependency = Annotated[Session, Depends(get_session)]
admin_dependency = Annotated[User, Depends(get_current_admin)]


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(new_product: ProductCreate, session: session_dependency, admin: admin_dependency):
    return create_product_service(new_product, session, admin)


@router.get("/", response_model=list[ProductRead])
def get_all_products(
    session: session_dependency,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 50,
):
    return get_products_service(session, page, limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, session: session_dependency):
    return get_product_by_id_service(product_id, session)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, session: session_dependency, admin: admin_dependency):
    return update_product_service(product_id, payload, session, admin)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: session_dependency, admin: admin_dependency):
    delete_product_service(product_id, session, admin)