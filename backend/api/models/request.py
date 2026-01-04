"""Request models for API endpoints."""

from pydantic import BaseModel, Field


class CityInformationRequest(BaseModel):
    """Request model for city information endpoint."""

    adress_in: str = Field(..., description="Adresse à analyser", min_length=1)
