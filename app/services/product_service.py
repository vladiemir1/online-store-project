from app.models.product import Product
from typing import List

INITIAL_PRODUCTS = [
    Product(id=1, name="Чайник", price=1500.0, seller_id=1, description="Электрический чайник"),
    Product(id=2, name="Телефон", price=25000.0, seller_id=1, description="Смартфон"),
]
PRODUCTS_DB: List[Product] = list(INITIAL_PRODUCTS)
class ProductService:
    """Сервис работы с товарами."""
    
    def create_product(self, name: str, price: float, seller_id: int, description: str) -> Product:
        # В этой простой модели ID генерируется на основе текущей длины списка
        new_id = len(PRODUCTS_DB) + 1
        new_product = Product(id=new_id, name=name, price=price, seller_id=seller_id, description=description)
        
        # Добавляем новый товар в список
        PRODUCTS_DB.append(new_product)
        
        return new_product

    def get_products_by_seller(self, seller_id: int) -> List[Product]:
        """возвращает список товаров, конкретного продавца."""
        return [p for p in PRODUCTS_DB if p.seller_id == seller_id]
        
    def get_all_products(self) -> List[Product]:
        unique_products_map = {p.id: p for p in PRODUCTS_DB}
        return list(unique_products_map.values())