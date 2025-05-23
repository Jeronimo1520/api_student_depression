from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import prediction
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    prediction.router,
    prefix=settings.API_V1_STR,
    tags=["predictions"]
)

@app.get("/")
async def root():
    """
    Root endpoint that returns API information.
    """
    return {
        "message": "Welcome to the Random Forest Prediction API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 