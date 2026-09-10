import requests
import streamlit as st

from streamlit_geolocation import streamlit_geolocation
from services.geocoder import geocode_location
from services.router import (
    get_route,
    get_route_road_names,
)
from services.weather import get_weather
from ui.map import display_route_map
from services.incident_search import search_route_incidents
from services.incident_analyzer import analyze_route_incidents
from ui.travel_brief import generate_travel_brief

st.set_page_config(
    page_title="RouteGuard",
    page_icon="🚗",
    layout="wide",
)


st.title("🚗 RouteGuard")
st.caption("Smart Route & Travel Alert Assistant")

st.write(
    "Plan your journey, check current conditions, "
    "and get alerts about potential route disruptions."
)

st.divider()


st.subheader("📍 Current Location")

gps_location = streamlit_geolocation()

if gps_location and gps_location.get("latitude") is not None:

    st.success("📍 Current location detected.")

    gps_latitude = gps_location["latitude"]
    gps_longitude = gps_location["longitude"]

    st.write(
        f"Latitude: {gps_latitude:.6f}"
    )

    st.write(
        f"Longitude: {gps_longitude:.6f}"
    )

else:

    gps_latitude = None
    gps_longitude = None

    st.info(
        "GPS location is not available. "
        "You can enter your location manually below."
    )

current_location = st.text_input(
    "Or enter your location manually",
    placeholder="Example: Gulistan-e-Jauhar, Karachi",
)

destination = st.text_input(
    "🏁 Destination",
    placeholder="Example: Port Qasim, Karachi",
)


if st.button("🚗 Plan My Route", type="primary"):

    if not current_location or not destination:
        st.warning(
            "Please enter both your current location and destination."
        )

    else:

        with st.spinner("Finding locations..."):

            try:
                origin = geocode_location(current_location)
                destination_data = geocode_location(destination)

            except requests.RequestException:
                st.error(
                    "Unable to contact the location service. "
                    "Please try again later."
                )

            else:

                if origin is None:
                    st.error(
                        f"Could not find: {current_location}"
                    )

                elif destination_data is None:
                    st.error(
                        f"Could not find: {destination}"
                    )

                else:

                    st.success("Both locations found successfully!")
                                        with st.spinner("Calculating route..."):

                        try:
                            route = get_route(
                                origin,
                                destination_data,
                            )

                        except requests.RequestException:
                            st.error(
                                "Unable to contact the routing service. "
                                "Please try again later."
                            )
                            route = None

                    if route is None:
                        st.error(
                            "Unable to calculate a route "
                            "between these locations."
                        )

                    else:
                        st.success("Route calculated successfully!")
                        road_names = get_route_road_names(
                            route["steps"]
                        )

                                            st.subheader("⚠️ Route Alerts")

                        with st.spinner(
                            "Searching for recent incidents "
                            "on your route..."
                        ):

                            try:

                                raw_incidents = search_route_incidents(
                                    road_names
                                )

                                route_incidents = analyze_route_incidents(
                                    raw_incidents,
                                    road_names,
                                )

                            except requests.RequestException:

                                st.warning(
                                    "Unable to search for route incidents "
                                    "at this time."
                                )

                                route_incidents = []

                        if route_incidents:

    st.warning(
        f"{len(route_incidents)} "
        f"potential route incident(s) found."
    )

    for incident in route_incidents:

        with st.expander(
            f"🚨 {incident['type']} — "
            f"{incident['road']}"
        ):

            st.write(
                f"**Incident:** "
                f"{incident['title']}"
            )

            st.write(
                f"**Freshness:** "
                f"{incident['freshness']}"
            )

            st.write(
                f"**Confidence:** "
                f"{incident['confidence']}"
            )

            st.write(
                f"**Source:** "
                f"{incident['source']}"
            )

            if incident["url"]:
                st.write(
                    f"[Read source]({incident['url']})"
                )

else:

    st.success(
        "✅ No relevant recent route incidents "
        "were found."
    )

                            for incident in route_incidents:

                                st.markdown(
                                    f"### 🚨 {incident['type']}"
                                )

                                st.write(
                                    f"**Road:** "
                                    f"{incident['road']}"
                                )

                                st.write(
                                    f"**Incident:** "
                                    f"{incident['title']}"
                                )

                                st.write(
                                    f"**Freshness:** "
                                    f"{incident['freshness']}"
                                )

                                st.write(
                                    f"**Confidence:** "
                                    f"{incident['confidence']}"
                                )

                                st.write(
                                    f"**Source:** "
                                    f"{incident['source']}"
                                )

                                if incident["url"]:

                                    st.write(
                                        f"[Read source]({incident['url']})"
                                    )

                                st.divider()

                        else:

                            st.success(
                                "No relevant recent route incidents "
                                "were found."
                            )    

                       col1, col2 = st.columns(2)

                       with col1:
                         st.metric(
                           "🛣️ Distance",
                           f"{route['distance_km']:.1f} km",
                         )

                       with col2:
                         st.metric(
                          "⏱️ Estimated Time",
                          f"{route['duration_minutes']:.0f} min",
                         )
                            st.subheader("🛣️ Route Roads")

                        if road_names:

                            for road in road_names:
                                st.write(f"• {road}")

                        else:
                            st.info(
                                "No named roads were found "
                                "for this route."
                            )
                        st.subheader("🗺️ Route Map")

                        display_route_map(
                            origin,
                            destination_data,
                            route,
                        )
                        st.subheader("🌤️ Current Weather at Starting Location")

                        with st.spinner("Getting current weather..."):

                            try:
                                weather = get_weather(
                                    origin["latitude"],
                                    origin["longitude"],
                                )

                            except requests.RequestException:
                                st.warning(
                                    "Unable to retrieve current weather."
                                )
                                weather = None

                        if weather:

                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                st.metric(
                                    "Temperature",
                                    f"{weather['temperature']} °C",
                                )

                            with col2:
                                st.metric(
                                    "Humidity",
                                    f"{weather['humidity']} %",
                                )

                            with col3:
                                st.metric(
                                    "Condition",
                                    weather["description"],
                                )

                            with col4:
                                st.metric(
                                    "Wind Speed",
                                    f"{weather['wind_speed']} km/h",
                                )   

                    st.subheader("📋 Travel Brief")

with st.container(border=True):

    travel_brief = generate_travel_brief(
        route,
        weather,
        route_incidents,
    )

    for item in travel_brief:
        st.write(item)

st.caption(
    "⚠️ RouteGuard alerts are based on available public "
    "information and may not represent real-time road "
    "conditions. Always follow official traffic "
    "instructions and road signs."
)
       
                    st.subheader("📍 Current Location")

                    st.write(origin["display_name"])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Latitude",
                            f"{origin['latitude']:.6f}",
                        )

                    with col2:
                        st.metric(
                            "Longitude",
                            f"{origin['longitude']:.6f}",
                        )

                    st.subheader("🏁 Destination")

                    st.write(destination_data["display_name"])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Latitude",
                            f"{destination_data['latitude']:.6f}",
                        )

                    with col2:
                        st.metric(
                            "Longitude",
                            f"{destination_data['longitude']:.6f}",
                        )
