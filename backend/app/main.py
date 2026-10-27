from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import engine
from app.api.auth import router as auth_router
from app.api.admin_staff import router as admin_staff_router
from app.core.config import settings

app = FastAPI(
    title="Customer Support API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_staff_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}


