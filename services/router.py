import requests


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(origin, destination):
    """
    Calculate a driving route between two locations using OSRM.

    Parameters:
        origin (dict): Location containing latitude and longitude.
        destination (dict): Location containing latitude and longitude.

    Returns:
        dict: Route information.
        None: If no route is found.
    """

    origin_coordinates = (
        f"{origin['longitude']},{origin['latitude']}"
    )

    destination_coordinates = (
        f"{destination['longitude']},{destination['latitude']}"
    )

    coordinates = (
        f"{origin_coordinates};{destination_coordinates}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "alternatives": "false",
    }

    url = f"{OSRM_URL}/{coordinates}"

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        return None

    if not data.get("routes"):
        return None

    route = data["routes"][0]

    return {
        "distance_km": route["distance"] / 1000,
        "duration_minutes": route["duration"] / 60,
        "geometry": route["geometry"],
        "steps": route["legs"][0]["steps"],
    }
