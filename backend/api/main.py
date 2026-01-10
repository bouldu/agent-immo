"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.endpoints import city_information
from backend.config import settings
from backend.utils.langsmith_init import init_langsmith

# Initialize LangSmith
init_langsmith()

app = FastAPI(
    title="AgentImmo API",
    description="API pour l'analyse immobilière avec agents LangGraph",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(city_information.router, tags=["city-information"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AgentImmo API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
