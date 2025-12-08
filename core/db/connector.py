from typing import Optional, Dict
from core.models.user_model import UserModel, UserEntity
from core.security.password_hasher import PasswordHasher
from core.security.validator import Validator


USER_DATABASE: Dict[int, UserEntity] = {}
next_id = 1

class FakeUserModel(UserModel):
    
    def create_user(self, login: str, email: str, password_hash: str, role: str) -> UserEntity:
        global next_id
        if self.get_by_login(login):
            raise ValueError("Пользователь с таким логином уже существует.")
        
        user = UserEntity(
            id=next_id,
            login=login,
            email=email,
            password_hash=password_hash,
            role=role
        )
        USER_DATABASE[next_id] = user
        next_id += 1
        return user

    def get_by_login(self, login: str) -> Optional[UserEntity]:
        for user in USER_DATABASE.values():
            if user.login == login:
                return user
        return None

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        return USER_DATABASE.get(user_id)

# юзаем все наши кор классы 
user_model: UserModel = FakeUserModel()
hasher = PasswordHasher()
validator = Validator()