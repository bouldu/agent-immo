"""Request models for API endpoints."""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request model for analyze endpoint."""

    adresse: str = Field(..., description="Adresse à analyser", min_length=1)






