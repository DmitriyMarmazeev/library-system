from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.books.router import router as books_router
from app.modules.copies.router import router as copies_router
# from app.modules.loans.router import router as loans_router

app = FastAPI(
    title="Library Management System",
    version="1.0.0",
    description="Клиент-серверное приложение для управления библиотекой"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(books_router, prefix="/api/v1/books", tags=["Books"])
app.include_router(copies_router, prefix="/api/v1/copies", tags=["Copies"])
# app.include_router(loans_router, prefix="/api/v1/loans", tags=["Loans"])

@app.get("/")
async def root():
    return {
        "message": "Library Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}