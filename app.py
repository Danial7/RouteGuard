import requests
import streamlit as st

from services.geocoder import geocode_location
from services.router import get_route
from services.weather import get_weather
from ui.map import display_route_map


st.set_page_config(
    page_title="RouteGuard",
    page_icon="🚗",
    layout="wide",
)


st.title("🚗 RouteGuard")
st.subheader("Smart Route & Travel Alert Assistant")

st.write(
    "Enter your current location and destination "
    "to begin planning your journey."
)

st.divider()


current_location = st.text_input(
    "📍 Current Location",
    placeholder="Example: Gulistan-e-Jauhar, Karachi",
)

destination = st.text_input(
    "🏁 Destination",
    placeholder="Example: Port Qasim, Karachi",
)


if st.button("Find Coordinates", type="primary"):

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

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Distance",
                                f"{route['distance_km']:.2f} km",
                            )

                        with col2:
                            st.metric(
                                "Estimated Travel Time",
                                f"{route['duration_minutes']:.0f} min",
                            )

                        st.subheader("🗺️ Route Map")

                        display_route_map(
                            origin,
                            destination_data,
                            route,
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
