"""Cadastral parcel utilities for geocoding addresses and retrieving parcel information."""

import json
from typing import Any

import httpx


async def geocode_address(address: str) -> dict[str, Any]:
    """
    Geocode an address using the API Adresse to get coordinates.

    Args:
        address: The address to geocode (e.g., "10 rue de la Paix, 75002 Paris")

    Returns:
        Dictionary containing geocoding results with keys:
        - latitude: float
        - longitude: float
        - full_address: str (formatted address)
        - score: float (confidence score)
        - city: str
        - postcode: str

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If no address is found
    """
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": address, "limit": 1}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("features"):
            raise ValueError(f"Adresse non trouvée: {address}")

        feature = data["features"][0]
        properties = feature["properties"]
        coordinates = feature["geometry"]["coordinates"]

        return {
            "latitude": coordinates[1],
            "longitude": coordinates[0],
            "full_address": properties.get("label", address),
            "score": properties.get("score", 0.0),
            "city": properties.get("city", ""),
            "postcode": properties.get("postcode", ""),
            "raw_response": feature,
        }


async def get_cadastral_parcel(lat: float, lon: float) -> dict[str, Any]:
    """
    Get cadastral parcel information from coordinates using API Carto Cadastre.

    Args:
        lat: Latitude (WGS84)
        lon: Longitude (WGS84)

    Returns:
        Dictionary containing parcel information with keys:
        - parcel_id: str (parcelle identifier)
        - section: str
        - number: str
        - commune: str
        - geometry: dict (GeoJSON geometry)
        - raw_response: dict (full API response)

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If no parcel is found for the given coordinates
    """
    url = "https://apicarto.ign.fr/api/cadastre/parcelle"

    # Format GeoJSON POINT pour l'API Carto
    # dict to json string
    geom = json.dumps({"type": "Point", "coordinates": [lon, lat]})
    params = {"geom": geom}

    async with httpx.AsyncClient(timeout=10.0) as client:
        print("requesting url", url, "with params", params)
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or not isinstance(data.get("features"), list) or len(data.get("features")) == 0:
            raise ValueError(
                f"Aucune parcelle cadastrale trouvée pour les coordonnées ({lat}, {lon})"
            )

        parcel = data["features"][0]
        properties = parcel.get("properties", {})

        return {
            "parcel_id": properties.get("id", ""),
            "section": properties.get("section", ""),
            "number": properties.get("numero", ""),
            "commune": properties.get("nom_com", ""),
            "geometry": parcel.get("geometry", {}),
            "raw_response": parcel,
        }


async def get_parcel_from_address(address: str) -> dict[str, Any]:
    """
    Get cadastral parcel information from an address.

    This function combines geocoding and cadastral parcel retrieval.

    Args:
        address: The address to process (e.g., "10 rue de la Paix, 75002 Paris")

    Returns:
        Dictionary containing both geocoding and parcel information with keys:
        - address: dict (geocoding results from geocode_address)
        - parcel: dict (parcel information from get_cadastral_parcel)

    Raises:
        httpx.HTTPStatusError: If any API request fails
        ValueError: If address or parcel is not found
    """
    # Step 1: Geocode the address
    geocoding_result = await geocode_address(address)

    # Step 2: Get cadastral parcel
    parcel_result = await get_cadastral_parcel(
        geocoding_result["latitude"], geocoding_result["longitude"]
    )

    return {
        "address": geocoding_result,
        "parcel": parcel_result,
    }
