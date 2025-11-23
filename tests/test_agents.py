"""Unit tests for agents."""


from backend.agents.analyzer import AnalyzerAgent
from backend.agents.data_collector import DataCollectorAgent
from backend.agents.report_builder import ReportBuilderAgent
from backend.agents.visualizer import VisualizerAgent


def test_data_collector_agent():
    """Test DataCollectorAgent."""
    agent = DataCollectorAgent()
    result = agent.run({"adresse": "Paris, France"})
    assert "adresse" in result
    assert result["adresse"] == "Paris, France"


def test_analyzer_agent():
    """Test AnalyzerAgent."""
    agent = AnalyzerAgent()
    dataset = {"adresse": "Paris, France", "dvf_data": {}, "insee_data": {}, "open_data": {}}
    result = agent.run({"dataset": dataset})
    assert "prix_m2_moyen" in result


def test_visualizer_agent():
    """Test VisualizerAgent."""
    agent = VisualizerAgent()
    indicators = {"prix_m2_moyen": 5000}
    result = agent.run({"indicators": indicators})
    assert "price_chart" in result


def test_report_builder_agent():
    """Test ReportBuilderAgent."""
    agent = ReportBuilderAgent()
    indicators = {"prix_m2_moyen": 5000}
    images = {"price_chart": "chart.png"}
    result = agent.run({"indicators": indicators, "images": images})
    assert "pdf_path" in result






