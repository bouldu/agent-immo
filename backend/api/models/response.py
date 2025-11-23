"""Response models for API endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    """Response model for analyze endpoint."""

    workflow_id: str = Field(..., description="Identifiant unique du workflow")


class StatusResponse(BaseModel):
    """Response model for status endpoint."""

    workflow_id: str = Field(..., description="Identifiant unique du workflow")
    status: str = Field(..., description="État actuel du workflow")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progression (0.0 à 1.0)")
    results: dict[str, Any] | None = Field(
        None, description="Résultats intermédiaires disponibles"
    )
    error: str | None = Field(None, description="Message d'erreur si échec")


class ReportResponse(BaseModel):
    """Response model for report endpoint."""

    workflow_id: str = Field(..., description="Identifiant unique du workflow")
    pdf_bytes: bytes = Field(..., description="Contenu du PDF en bytes")
    filename: str = Field(..., description="Nom du fichier PDF")

