import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.api.v1.endpoints import auth_router, public_router, seller_router, customer_router 


# пока локально -  разрешаем все источники (*).
ALLOWED_ORIGINS = [
    "*", ]

app = FastAPI(
    title="Online Store",
    description="Бэкенд магазина"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы get, post, option
    allow_headers=["*"], # Разрешаем все заголовк
)
# -----------------------------------


# подключаем роутеры
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth (Core)"])
app.include_router(public_router.router, prefix="/api/v1", tags=["Public"])
app.include_router(seller_router.router, prefix="/api/v1/seller", tags=["Seller LK"])
app.include_router(customer_router.router, prefix="/api/v1/customer", tags=["Customer LK"])


@app.get("/api/v1/status", tags=["Public"])
def read_root():
    """Проверка доступности API."""
    return {"status": "OK", "message": "Store API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)