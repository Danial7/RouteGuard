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
