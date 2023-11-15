from fastapi import FastAPI, APIRouter

from .routers import users, products
from .database import Base, engine

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

app.include_router(
    users.router,
    prefix="/user",
)
app.include_router(
    products.router,
    prefix="/product",
)
