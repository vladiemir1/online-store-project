import re

class Validator:
    """
    класс для валидации данных).
    """
    @staticmethod
    def validate_register_data(data):
        if len(data.login) < 3 or len(data.login) > 50:
            raise ValueError("Логин должен содержать от 3 до 50 символов.")
        
        if len(data.password) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов.")
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
             raise ValueError("Некорректный формат E-mail.")
             
        if data.role not in ["ROLE_CUSTOMER", "ROLE_SELLER"]:
             raise ValueError("Недопустимая роль.")
             
        return True