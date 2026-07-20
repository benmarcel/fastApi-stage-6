from fastapi import HTTPException, status
from sqlmodel import Session, select
from model.product import Product, ProductCreate, ProductUpdate
from model.user import User


def get_products_service(session: Session, page: int, limit: int):
    offset = (page - 1) * limit
    db_query = select(Product).offset(offset).limit(limit)
    return session.exec(db_query).all()


def get_product_by_id_service(product_id: int, session: Session) -> Product:
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def create_product_service(new_product: ProductCreate, session: Session, admin: User):
    
    if admin.id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin ID is required to create a product.")
    product_data = new_product.model_dump()
    product_data["admin_id"] = admin.id
    product = Product.model_validate(product_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product_service(product_id: int, payload: ProductUpdate, session: Session, admin: User) -> Product:
    product = get_product_by_id_service(product_id, session)
    _ensure_product_owner(product, admin)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product_service(product_id: int, session: Session, admin: User) -> None:
    product = get_product_by_id_service(product_id, session)
    _ensure_product_owner(product, admin)
    session.delete(product)
    session.commit()


def _ensure_product_owner(product: Product, admin: User) -> None:
    if product.admin_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this product.",
        )