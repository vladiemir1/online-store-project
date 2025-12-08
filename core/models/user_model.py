from typing import Optional, Dict

class UserEntity:
    """Сущность пользователя. Объект для передачи данных."""
    def __init__(self, id: int, login: str, email: str, password_hash: str, role: str):
        self.id = id
        self.login = login
        self.email = email
        self.password_hash = password_hash
        self.role = role 

class UserModel:
    """
    Абстрактный класс модели пользователя.
    """
    def create_user(self, login: str, email: str, password_hash: str, role: str) -> UserEntity:
        raise NotImplementedError

    def get_by_login(self, login: str) -> Optional[UserEntity]:
        raise NotImplementedError

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        raise NotImplementedError