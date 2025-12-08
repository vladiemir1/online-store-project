from fastapi import APIRouter, Depends
from core.dependencies.auth_guard import get_customer
from core.models.user_model import UserEntity

router = APIRouter()


@router.get("/cart")
def view_cart(customer: UserEntity = Depends(get_customer)):
    """Доступен только покупателям - проверяет через authguard"""
    return {"message": f"Корзина пользователя {customer.login}", "items": []}


@router.post("/checkout")
def checkout(customer: UserEntity = Depends(get_customer)):
    """Оформление покупки."""
    return {"message": f"Заказ успешно оформлен для пользователя {customer.login}"}