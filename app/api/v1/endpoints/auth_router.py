from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from core.db.connector import user_model, hasher, validator
from core.security.session_manager import SessionManager
from core.dependencies.auth_guard import get_current_user
from core.models.user_model import UserEntity

router = APIRouter()
session_manager = SessionManager()

# регистрация польз
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest):
    """Использует Validator, PasswordHasher и UserModel."""
    try:
        validator.validate_register_data(request)
        hashed_password = hasher.hash_password(request.password)
        
        new_user = user_model.create_user(
            login=request.login,
            email=request.email,
            password_hash=hashed_password,
            role=request.role
        )
        
        token = session_manager.create_session(new_user.id, new_user.role)
        
        return AuthResponse(token=token, user_id=new_user.id, role=new_user.role)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# авторизация уже зареанного
@router.post("/login", response_model=AuthResponse)
def login_user(request: LoginRequest):
    """Использует с UserModelwq, PasswordHasher и SessionManager."""
    user = user_model.get_by_login(request.login)

    if not user or not hasher.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль."
        )
    
    token = session_manager.create_session(user.id, user.role)
    
    return AuthResponse(token=token, user_id=user.id, role=user.role)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(user: UserEntity = Depends(get_current_user)):
    return {"message": f"Пользователь {user.login} вышел из системы."}

# проверка на тип акка
@router.get("/profile", response_model=UserResponse)
def get_user_profile(user: UserEntity = Depends(get_current_user)):
    """Доступно (AuthGuard)."""
    return UserResponse(
        id=user.id,
        login=user.login,
        email=user.email,
        role=user.role
    )