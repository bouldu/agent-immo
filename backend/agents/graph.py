from langgraph.graph import END, START, StateGraph

from backend.agents.city_information.agent import city_information
from backend.agents.state import MarketStudyState


# memory = InMemorySaver()
def create_agent() -> StateGraph:
    builder = StateGraph(MarketStudyState)

    builder.add_node("city_information", city_information)
    builder.add_edge(START, "city_information")

    builder.add_edge("city_information", END)

    agent = builder.compile()
    return agent


market_study_agent = create_agent()
