import jwt
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone 

# ключ для кодирования 
SECRET_KEY = "32b260f8983e20d588f6c4c5f9b5c2c77f041e247a329158428414441314949a" 
ALGORITHM = "HS256"
# Время жизни токена
SESSION_EXPIRE_MINUTES = 30 


class SessionManager:
    """ 
    класс для создания, декодинга и кодинга токенов.
    """
    
    def create_session(self, user_id: int, role: str) -> str:
        """
        выдается jwt токен новому пользователю.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES)
        
        payload: Dict[str, Any] = {
            "sub": str(user_id), 
            "role": role,
            "exp": expire, 
            "iat": datetime.now(timezone.utc)
        }
        
        
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def validate_session(self, token: str) -> Optional[dict]:
        """
        декодинг и валдиция jwt.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError as e:
            # логи для проверки 401 
            print(f"!!! JWT DECODING ERROR: {e}") 
            return None