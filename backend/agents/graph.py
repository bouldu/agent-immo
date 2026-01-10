from langgraph.graph import END, START, StateGraph

from backend.agents.city_information.agent import get_city_information
from backend.agents.state import CityInformationState


# memory = InMemorySaver()
def create_agent() -> StateGraph:
    builder = StateGraph(CityInformationState)

    builder.add_node("city_information", get_city_information)
    builder.add_edge(START, "city_information")

    builder.add_edge("city_information", END)

    agent = builder.compile()
    return agent


city_information_agent = create_agent()
