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
