from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

from backend.agents.city_information.prompt import PROMPT_CITY_INFORMATION
from backend.agents.city_information.state import CityInformation
from backend.agents.state import CityInformationState

city_information_agent = create_agent(
    "mistral-small-latest",
    system_prompt=SystemMessage(PROMPT_CITY_INFORMATION),
    tools=[DuckDuckGoSearchRun()],
    response_format=CityInformation,
)


def get_city_information(city_name: str) -> CityInformationState:
    messages = [HumanMessage(city_name)]

    ai_response = city_information_agent.invoke({"messages": messages})

    # ai_messages = ai_response["messages"]
    # print(ai_messages)

    city_information: CityInformationState = ai_response["structured_response"]

    return city_information
