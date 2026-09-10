import requests


GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def search_incidents(road_name):
    """
    Search recent public news information for a road.
    """

    query = (
        f'"{road_name}" '
        f'(accident OR crash OR traffic OR congestion OR '
        f'closure OR construction OR diversion OR blocked)'
    )

    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": 10,
        "sort": "datedesc",
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
