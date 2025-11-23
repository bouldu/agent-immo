from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.agents.city_information.prompt import PROMPT_CITY_INFORMATION
from backend.agents.city_information.state import CityInformation
from backend.agents.common_tools import extract_json_from_ai_message
from backend.agents.state import MarketStudyState

llm = ChatOllama(
    model="gemma3",
    temperature=0,
    # other params...
)


def city_information(state: MarketStudyState) -> MarketStudyState:
    messages = [SystemMessage(PROMPT_CITY_INFORMATION), HumanMessage(state["adress_in"])]

    ai_msg = llm.invoke(messages)

    json_content: CityInformation = extract_json_from_ai_message(ai_msg)
    return {**state, "city_information": json_content}
