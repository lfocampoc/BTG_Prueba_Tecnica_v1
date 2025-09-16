from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.api.routes import router
from src.config import settings
from src.exceptions import BTGException

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando BTG Pactual Funds API...")
    yield
    print("🛑 Cerrando BTG Pactual Funds API...")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para gestión de fondos de inversión BTG Pactual",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(BTGException)
async def btg_exception_handler(request, exc: BTGException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}

# Include routers
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=settings.debug)