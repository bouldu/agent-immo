"""Analyze endpoint for launching workflow."""

import asyncio

from fastapi import APIRouter

from backend.api.models.request import AnalyzeRequest
from backend.api.models.response import AnalyzeResponse
from backend.workflow import orchestrator

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Launch analysis workflow for an address.

    Args:
        request: AnalyzeRequest containing the address

    Returns:
        AnalyzeResponse with workflow_id
    """
    # Create workflow
    workflow_id = orchestrator.create_workflow(request.adresse)

    # Run workflow asynchronously
    asyncio.create_task(orchestrator.run_workflow(workflow_id))

    return AnalyzeResponse(workflow_id=workflow_id)






