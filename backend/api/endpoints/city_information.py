"""City information endpoint for executing city information agent."""

from fastapi import APIRouter

from backend.agents.city_information import get_city_information
from backend.api.models.request import CityInformationRequest
from backend.api.models.response import CityInformationResponse

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
    city_info_response = get_city_information(request.adress_in)

    return CityInformationResponse(
        adress_in=request.adress_in,
        messages=[],
        city_information=city_info_response,
    )
