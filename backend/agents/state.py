from typing import TypedDict

from langchain_core.messages import BaseMessage

from backend.agents.city_information.state import CityInformation


class MarketStudyState(TypedDict):
    adress_in: str
    messages: list[BaseMessage]
    city_information: CityInformation
