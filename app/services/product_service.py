from app.models.product import Product
from typing import List

PRODUCTS_DB: List[Product] = [
    Product(id=1, name="Чайник", price=1500.0, seller_id=1, description="Электрический чайник"),
    Product(id=2, name="Телефон", price=25000.0, seller_id=1, description="Смартфон"),
]

class ProductService:
    """работа с товарами."""
    def create_product(self, name: str, price: float, seller_id: int, description: str) -> Product:
        new_id = len(PRODUCTS_DB) + 1
        new_product = Product(id=new_id, name=name, price=price, seller_id=seller_id, description=description)
        PRODUCTS_DB.append(new_product)
        return new_product

    def get_products_by_seller(self, seller_id: int) -> List[Product]:
        return [p for p in PRODUCTS_DB if p.seller_id == seller_id]
        
    def get_all_products(self) -> List[Product]:
        return PRODUCTS_DB