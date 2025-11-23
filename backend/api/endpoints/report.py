"""Report endpoint for downloading PDF report."""

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.workflow import orchestrator

router = APIRouter()


@router.get("/report/{workflow_id}")
async def get_report(workflow_id: str) -> FileResponse:
    """
    Download the final PDF report.

    Args:
        workflow_id: Unique workflow identifier

    Returns:
        PDF file response
    """
    workflow = orchestrator.get_workflow_status(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    if workflow["status"] != "completed":
        raise HTTPException(
            status_code=400, detail=f"Workflow {workflow_id} is not completed yet"
        )

    report_path = workflow.get("results", {}).get("report", {}).get("pdf_path")

    if not report_path or not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"rapport_{workflow_id}.pdf",
    )






