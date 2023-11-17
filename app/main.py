from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, products, keywords, deals, notices
from .database import Base, engine

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:5173", "http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

app.include_router(
    users.router,
    prefix="/user",
    tags=["user"],
)
app.include_router(
    products.router,
    prefix="/product",
    tags=["product"],
)
app.include_router(
    keywords.router,
    prefix="/keyword",
    tags=["keyword"],
)
app.include_router(
    deals.router,
    prefix="/deal",
    tags=["deal"],
)

app.include_router(
    notices.router,
    prefix="/notice",
    tags=["notice"],
)
