import requests


GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def search_incidents(road_name):
    """
    Search recent public reports for a specific road.
    """

    query = (
        f'"{road_name}" Karachi '
        f'(accident OR crash OR collision OR '
        f'"traffic jam" OR congestion OR '
        f'"road closure" OR "road closed" OR '
        f'construction OR diversion OR '
        f'"road blocked" OR "lane closure")'
    )

    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": 10,
        "sort": "datedesc",
        "timespan": "7d",
    }

    response = requests.get(
        GDELT_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

    incidents = []

    for article in articles:

        incidents.append(
            {
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("domain", ""),
                "published": article.get("seendate", ""),
                "language": article.get("language", ""),
                "road": road_name,
            }
        )

    return incidents

    def search_route_incidents(road_names):
    """
    Search for incidents on all roads in a route.
    """

    all_incidents = []

    for road_name in road_names:

        try:
            incidents = search_incidents(road_name)

            all_incidents.extend(incidents)

        except requests.RequestException:
            print(
                f"Could not search incidents for: "
                f"{road_name}"
            )

    return all_incidents
