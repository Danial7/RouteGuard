INCIDENT_KEYWORDS = {
    "ACCIDENT": [
        "accident",
        "crash",
        "collision",
        "hit",
        "overturned",
    ],

    "TRAFFIC_CONGESTION": [
        "traffic jam",
        "traffic congestion",
        "heavy traffic",
        "traffic gridlock",
        "congested",
        "traffic disruption",
    ],

    "ROAD_CLOSURE": [
        "road closed",
        "road closure",
        "road shut",
        "road blocked",
        "closed for traffic",
    ],

    "LANE_CLOSURE": [
        "lane closed",
        "lane closure",
        "lanes closed",
    ],

    "CONSTRUCTION": [
        "construction",
        "road work",
        "repair work",
        "development work",
        "under construction",
    ],

    "DIVERSION": [
        "diversion",
        "traffic diverted",
        "route diverted",
        "diverted traffic",
    ],

    "ROAD_BLOCKED": [
        "road blocked",
        "blocked road",
        "blocked for traffic",
        "traffic blocked",
    ],
}


def classify_incident(title):
    """
    Classify an incident based on keywords in its title.
    """

    text = title.lower()

    for incident_type, keywords in INCIDENT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:
                return incident_type

    return None

    from datetime import datetime, timezone


def calculate_freshness(published_time):
    """
    Estimate how recent an incident is.
    """

    if not published_time:
        return "UNKNOWN"

    try:
        published = datetime.strptime(
            published_time,
            "%Y%m%dT%H%M%SZ",
        ).replace(tzinfo=timezone.utc)

    except ValueError:
        return "UNKNOWN"

    now = datetime.now(timezone.utc)

    age_hours = (
        now - published
    ).total_seconds() / 3600

    if age_hours <= 6:
        return "VERY_RECENT"

    if age_hours <= 24:
        return "RECENT"

    def analyze_incident(incident):
    """
    Classify and assess the freshness of an incident.
    """

    incident_type = classify_incident(
        incident["title"]
    )

    freshness = calculate_freshness(
        incident["published"]
    )

    if incident_type is None:
        return None

    analyzed_incident = incident.copy()

    analyzed_incident["type"] = incident_type
    analyzed_incident["freshness"] = freshness

    return analyzed_incident

    if age_hours <= 72:
        return "OLDER"

    return "STALE"

    def calculate_route_relevance(incident, road_names):
    """
    Calculate how relevant an incident is to the selected route.
    """

    score = 0

    incident_road = incident.get("road", "").lower()

    route_roads = [
        road.lower()
        for road in road_names
    ]

    # Road match
    if incident_road in route_roads:
        score += 30

    # Freshness
    freshness = incident.get("freshness")

    if freshness == "VERY_RECENT":
        score += 25

    elif freshness == "RECENT":
        score += 20

    elif freshness == "OLDER":
        score += 10

    # Recognized incident
    if incident.get("type"):
        score += 10

    return score

    def get_confidence_level(score):
    """
    Convert relevance score into a confidence level.
    """

    if score >= 60:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    if score >= 20:
        return "LOW"

    return "IGNORE"
