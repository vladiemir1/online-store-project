from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from core.dependencies.auth_guard import get_seller
from core.models.user_model import UserEntity
from app.services.product_service import ProductService
from app.models.product import Product
from app.schemas.auth import UserResponse

router = APIRouter()
product_service = ProductService()


@router.get("/profile", response_model=UserResponse)
def get_seller_profile(seller: UserEntity = Depends(get_seller)):
    """Доступно только продавцам"""
    return UserResponse(
        id=seller.id,
        login=seller.login,
        email=seller.email,
        role=seller.role
    )


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_data: Product, seller: UserEntity = Depends(get_seller)):
    """Добавление нового товара."""
    new_product = product_service.create_product(
        name=product_data.name,
        price=product_data.price,
        seller_id=seller.id, 
        description=product_data.description
    )
    return new_product


@router.get("/products", response_model=List[Product])
def list_seller_products(seller: UserEntity = Depends(get_seller)):
    """Просмотр всех товаров,которые добавил продавец"""
    return product_service.get_products_by_seller(seller.id)