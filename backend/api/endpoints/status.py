"""Status endpoint for checking workflow status."""

from fastapi import APIRouter, HTTPException

from backend.api.models.response import StatusResponse
from backend.workflow import orchestrator

router = APIRouter()


@router.get("/status/{workflow_id}", response_model=StatusResponse)
async def get_status(workflow_id: str) -> StatusResponse:
    """
    Get workflow status and intermediate results.

    Args:
        workflow_id: Unique workflow identifier

    Returns:
        StatusResponse with current status and results
    """
    workflow = orchestrator.get_workflow_status(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    return StatusResponse(
        workflow_id=workflow["workflow_id"],
        status=workflow["status"],
        progress=workflow["progress"],
        results=workflow.get("results"),
        error=workflow.get("error"),
    )






