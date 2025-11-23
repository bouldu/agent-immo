"""Workflow orchestrator for LangGraph agents."""

import uuid
from typing import Any

from backend.agents.analyzer import AnalyzerAgent
from backend.agents.data_collector import DataCollectorAgent
from backend.agents.report_builder import ReportBuilderAgent
from backend.agents.visualizer import VisualizerAgent


class WorkflowOrchestrator:
    """Orchestrates the execution of LangGraph agents in sequence."""

    def __init__(self):
        """Initialize the workflow orchestrator."""
        self.data_collector = DataCollectorAgent()
        self.analyzer = AnalyzerAgent()
        self.visualizer = VisualizerAgent()
        self.report_builder = ReportBuilderAgent()
        self.workflows: dict[str, dict[str, Any]] = {}

    def create_workflow(self, adresse: str) -> str:
        """Create a new workflow instance."""
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            "workflow_id": workflow_id,
            "adresse": adresse,
            "status": "pending",
            "progress": 0.0,
            "results": {},
            "error": None,
        }
        return workflow_id

    def get_workflow_status(self, workflow_id: str) -> dict[str, Any]:
        """Get the status of a workflow."""
        return self.workflows.get(workflow_id, {})

    async def run_workflow(self, workflow_id: str) -> None:
        """Run the complete workflow for a given workflow_id."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.workflows[workflow_id]

        try:
            # Step 1: Data Collection
            workflow["status"] = "collecting"
            workflow["progress"] = 0.25
            dataset = self.data_collector.run({"adresse": workflow["adresse"]})
            workflow["results"]["dataset"] = dataset

            # Step 2: Analysis
            workflow["status"] = "analyzing"
            workflow["progress"] = 0.5
            indicators = self.analyzer.run({"dataset": dataset})
            workflow["results"]["indicators"] = indicators

            # Step 3: Visualization
            workflow["status"] = "visualizing"
            workflow["progress"] = 0.75
            images = self.visualizer.run({"indicators": indicators})
            workflow["results"]["images"] = images

            # Step 4: Report Building
            workflow["status"] = "building_report"
            workflow["progress"] = 0.9
            report = self.report_builder.run(
                {"indicators": indicators, "images": images}
            )
            workflow["results"]["report"] = report

            # Complete
            workflow["status"] = "completed"
            workflow["progress"] = 1.0

        except Exception as e:
            workflow["status"] = "failed"
            workflow["error"] = str(e)
            raise


# Global orchestrator instance
orchestrator = WorkflowOrchestrator()






