"""City information endpoint for executing city information agent."""

from fastapi import APIRouter, HTTPException

from backend.agents.graph import city_information_agent
from backend.api.models.request import CityInformationRequest
from backend.api.models.response import CityInfoData, CityInformationResponse

router = APIRouter()


@router.post("/city-information", response_model=CityInformationResponse)
async def city_information(request: CityInformationRequest) -> CityInformationResponse:
    """
    Execute city information agent for an address.

    Args:
        request: CityInformationRequest containing the address

    Returns:
        CityInformationResponse with complete city information state
    """
    try:
        # Initialize state
        initial_state: dict = {
            "adress_in": request.adress_in,
            "messages": [],
            "city_information": {
                "situation": "",
                "politique_color": "",
                "qualitative_presentation": "",
            },
        }

        # Execute agent
        result_state = await city_information_agent.ainvoke(initial_state)

        # Convert messages to dict format for JSON serialization
        messages_dict = []
        if result_state.get("messages"):
            for msg in result_state["messages"]:
                if hasattr(msg, "content") and hasattr(msg, "type"):
                    messages_dict.append({"type": msg.type, "content": msg.content})
                else:
                    messages_dict.append(str(msg))

        # Convert city_information to response model
        city_info_response = None
        if result_state.get("city_information"):
            city_info = result_state["city_information"]
            city_info_response = CityInfoData(
                situation=city_info.get("situation", ""),
                politique_color=city_info.get("politique_color", ""),
                qualitative_presentation=city_info.get("qualitative_presentation", ""),
            )

        return CityInformationResponse(
            adress_in=result_state.get("adress_in", request.adress_in),
            messages=messages_dict,
            city_information=city_info_response,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error executing city information agent: {str(e)}"
        ) from e
