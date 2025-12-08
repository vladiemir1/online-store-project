from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    login: str
    password: str
    name: str 
    email: EmailStr 
    role: str = "ROLE_CUSTOMER" 

class LoginRequest(BaseModel):
    login: str
    password: str

class AuthResponse(BaseModel):
    message: str = "Авторизация успешна"
    token: str
    user_id: int
    role: str

class UserResponse(BaseModel):
    id: int
    login: str
    email: EmailStr
    role: str