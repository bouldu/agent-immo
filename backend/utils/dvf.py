"""DVF (Demande de Valeurs Foncières) API utilities for retrieving real estate transaction data."""

from typing import Any

import httpx


async def get_dvf_transactions(lat: float, lon: float, dist: int = 200) -> dict[str, Any]:
    """
    Get real estate transactions (DVF) data from coordinates using API CQuest DVF.

    Args:
        lat: Latitude (WGS84)
        lon: Longitude (WGS84)
        dist: Distance in meters around the point (default: 200)

    Returns:
        Dictionary containing DVF data with keys:
        - source: str (data source information)
        - derniere_maj: str (last update date)
        - licence: str (license URL)
        - transactions: list[dict] (list of transaction features)
        - raw_response: dict (full API response)

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If no transactions are found or response is invalid
    """

    # TODO : Pour le moment j'utilise https://api.cquest.org/dvf qui s'arrete en 2020
    # L'api DVF+ est restreinte et il faut faire un rdv pour y accéder. https://geoservices.sogefi-sig.com/documentation.php?doc=api_dvfplus_v1.0&api=dvfplus#/D%C3%A9couvrez%20les%20routes%20Sogefi
    # On peut aussi dl les fichiers csv et les upload soi meme sur un serveur local.
    # Sur le site https://explore.data.gouv.fr/fr/immobilier?onglet=carte&filtre=tous&lat=48.11645&lng=-1.68111&zoom=17.67&code=35238000AB0855&level=parcelle,
    # on peut voir qu'il appelle une api qui semble fonctionner sans authentification https://app.dvf.etalab.gouv.fr/api/mutations3/35238/000DK.
    # Ce n'est pas officiel donc à voir si on peut l'utiliser
    url = "https://api.cquest.org/dvf"
    params = {"lat": lat, "lon": lon, "dist": dist}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or data.get("type") != "Featurecollection":
            raise ValueError("Réponse invalide de l'API DVF")

        features = data.get("features", [])

        # Extract and format transaction data
        transactions = []
        for feature in features:
            props = feature.get("properties", {})
            transactions.append(
                {
                    "date_mutation": props.get("date_mutation"),
                    "nature_mutation": props.get("nature_mutation"),
                    "valeur_fonciere": props.get("valeur_fonciere"),
                    "type_local": props.get("type_local"),
                    "code_type_local": props.get("code_type_local"),
                    "surface_relle_bati": props.get("surface_relle_bati"),
                    "nombre_pieces_principales": props.get("nombre_pieces_principales"),
                    "surface_terrain": props.get("surface_terrain"),
                    "adresse": _format_address(props),
                    "coordonnees": {
                        "lat": props.get("lat"),
                        "lon": props.get("lon"),
                    },
                    "raw_properties": props,
                }
            )

        return {
            "source": data.get("source", ""),
            "derniere_maj": data.get("derniere_maj", ""),
            "licence": data.get("licence", ""),
            "transactions": transactions,
            "count": len(transactions),
            "raw_response": data,
        }


def _format_address(properties: dict[str, Any]) -> str:
    """
    Format address from DVF properties.

    Args:
        properties: DVF feature properties dictionary

    Returns:
        Formatted address string
    """
    parts = []
    if numero := properties.get("numero_voie"):
        parts.append(str(numero))
    if type_voie := properties.get("type_voie"):
        parts.append(type_voie)
    if voie := properties.get("voie"):
        parts.append(voie)
    if code_postal := properties.get("code_postal"):
        parts.append(code_postal)
    if commune := properties.get("commune"):
        parts.append(commune)

    return ", ".join(parts) if parts else "Adresse non disponible"
