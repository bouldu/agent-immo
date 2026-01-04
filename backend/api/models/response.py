"""Response models for API endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class CityInfoData(BaseModel):
    """City information data model."""

    situation: str = Field(..., description="Situation de la ville")
    politique_color: str = Field(..., description="Couleur politique de la ville")
    qualitative_presentation: str = Field(..., description="Présentation qualitative")


class CityInformationResponse(BaseModel):
    """Response model for city information endpoint."""

    adress_in: str = Field(..., description="Adresse analysée")
    messages: list[dict[str, Any]] = Field(default_factory=list, description="Messages de l'agent")
    city_information: CityInfoData | None = Field(None, description="Informations sur la ville")
