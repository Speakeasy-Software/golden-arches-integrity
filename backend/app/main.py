"""
Main FastAPI application for Golden Arches Integrity.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from .core.config import settings
from .core.azure_client import azure_client
from .api.endpoints import upload, analysis, annotation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Configure logging
    logger.remove()
    
    # Try to set up file logging, but don't fail if we can't
    try:
        # Use Azure App Service temp directory if available, otherwise skip file logging
        temp_dir = os.environ.get('TEMP', os.environ.get('TMP', '/tmp'))
        log_file = os.path.join(temp_dir, 'app.log')
        
        logger.add(
            log_file,
            format=settings.log_format,
            level=settings.log_level,
            rotation="1 day",
            retention="7 days"  # Reduced retention for Azure
        )
        logger.info(f"File logging enabled: {log_file}")
    except Exception as e:
        logger.warning(f"Could not set up file logging: {e}")
    
    # Always set up console logging
    logger.add(
        lambda msg: print(msg, end=""),
        format=settings.log_format,
        level=settings.log_level
    )
    
    # Initialize Azure clients
    try:
        await azure_client.initialize()
        logger.info("Azure services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Azure services: {e}")
        # Continue without Azure for development
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await azure_client.close()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered brand compliance checking for McDonald's Golden Arches",
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.azurewebsites.net", "testserver"]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": str(int(time.time()))
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else "Contact admin for API documentation",
        "health_check": "/health"
    }


# Include API routers
app.include_router(
    upload.router,
    prefix=f"{settings.api_v1_str}/upload",
    tags=["upload"]
)

app.include_router(
    analysis.router,
    prefix=f"{settings.api_v1_str}/analysis",
    tags=["analysis"]
)

app.include_router(
    annotation.router,
    prefix=f"{settings.api_v1_str}/annotation",
    tags=["annotation"]
)

# QA Portal routers - RE-ENABLED
from .api.endpoints import auth, review

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

app.include_router(
    review.router,
    prefix=f"{settings.api_v1_str}/review",
    tags=["review"]
)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 