from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from core.security.session_manager import SessionManager
from core.models.user_model import UserEntity
from core.db.connector import user_model 


session_manager = SessionManager()

async def get_current_user(token: Optional[str] = Header(None, alias="Authorization")) -> UserEntity:
    """
    AuthGuard: проверяет токен  и возвращает авторизованогой пользователя.
    """
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлен токен авторизации."
        )

    # Извлекаем чистый токен
    token = token.split(" ")[1]
    
    # Валидация сессии (декодирование)
    session_data = session_manager.validate_session(token)

    if not session_data:
        # Сюда попадаем, если токен просрочен, подделан или не совпадают SECRET_KEY
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или просроченный токен. Проверьте SECRET_KEY."
        )

    user_id_from_token = session_data.get("sub")
    try:
        
        user_id_for_db = int(user_id_from_token) 
    except (ValueError, TypeError):
        
        user_id_for_db = None
    
    if user_id_for_db is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат ID в токене.")

    
    print(f"!!! DEBUG AuthGuard: Ищем пользователя ID {user_id_for_db} (тип: {type(user_id_for_db)})")

    user = user_model.get_by_id(user_id_for_db)
    
    if not user:
        # если токен проверку на валид прошел, но юзера в бд нет
        print(f"!!! DEBUG AuthGuard: Пользователь с ID {user_id_for_db} НЕ НАЙДЕН в БД.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден.")

    return user

async def get_seller(user: UserEntity = Depends(get_current_user)):
    """Проверяет продавца."""
    if user.role != "ROLE_SELLER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуется роль Продавца."
        )
    return user

async def get_customer(user: UserEntity = Depends(get_current_user)):
    """Проверяет покупателя."""
    if user.role != "ROLE_CUSTOMER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуется роль Покупателя."
        )
    return user