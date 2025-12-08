from fastapi import APIRouter
from app.services.product_service import ProductService
from app.models.product import Product
from typing import List

router = APIRouter()
product_service = ProductService()


@router.get("/products", response_model=List[Product])
def list_all_products():
    """Просмотр всего каталога"""
    return product_service.get_all_products()