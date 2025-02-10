import streamlit as st
import requests


# Function to fetch weather data from Open-Meteo API
def get_weather(city):
    # Fetch geolocation of the city
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geocode_response = requests.get(geocode_url)

    if geocode_response.status_code != 200:
        return None

    location = geocode_response.json().get("results", [])
    if not location:
        return None

    latitude = location[0]["latitude"]
    longitude = location[0]["longitude"]

    # Now get weather data
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        return weather_response.json()
    else:
        return None


# Mapping WMO weather interpretation codes
wmo_weather_codes = {
    "0": "Clear sky",
    "1": "Mainly clear",
    "2": "Partly cloudy",
    "3": "Overcast",
    "45": "Fog",
    "48": "Depositing rime fog",
    "51": "Drizzle: Light intensity",
    "53": "Drizzle: Moderate intensity",
    "55": "Drizzle: Dense intensity",
    "56": "Freezing drizzle: Light intensity",
    "57": "Freezing drizzle: Dense intensity",
    "61": "Rain: Slight intensity",
    "63": "Rain: Moderate intensity",
    "65": "Rain: Heavy intensity",
    "66": "Freezing rain: Light intensity",
    "67": "Freezing rain: Heavy intensity",
    "71": "Snow fall: Slight intensity",
    "73": "Snow fall: Moderate intensity",
    "75": "Snow fall: Heavy intensity",
    "77": "Snow grains",
    "80": "Rain showers: Slight intensity",
    "81": "Rain showers: Moderate intensity",
    "82": "Rain showers: Violent intensity",
    "85": "Snow showers: Slight intensity",
    "86": "Snow showers: Heavy intensity",
    "95": "Thunderstorm: Slight or moderate",
    "96": "Thunderstorm with slight hail",
    "99": "Thunderstorm with heavy hail",
}

# Streamlit UI
st.title("Weather App.")

# Input for city name
city = st.text_input("Enter a city name (e.g., London, New York)")

if city:
    # Get weather data
    weather_data = get_weather(city)

    if weather_data:
        current_weather = weather_data["current_weather"]

        # Get weather code
        weather_code = str(current_weather["weathercode"])

        # Get the weather description from WMO codes
        weather_description = wmo_weather_codes.get(
            weather_code, "Unknown weather condition"
        )

        # Display weather information
        st.subheader(f"Weather in {city}")
        st.write(f"**Temperature**: {current_weather['temperature']}°C")
        st.write(f"**Wind Speed**: {current_weather['windspeed']} km/h")
        st.write(f"**Weather code**: {weather_code} ({weather_description})")

        # Display weather interpretation code tips
        with st.expander("**Weather Code Interpretation**"):
            st.markdown("**WMO Weather Codes**:")
            st.write(
                """
                - **0**: Clear sky
                - **1**: Mainly clear
                - **2**: Partly cloudy
                - **3**: Overcast
                - **45, 48**: Fog and depositing rime fog
                - **51, 53, 55**: Drizzle (Light, moderate, dense intensity)
                - **56, 57**: Freezing drizzle (Light, dense intensity)
                - **61, 63, 65**: Rain (Slight, moderate, heavy intensity)
                - **66, 67**: Freezing rain (Light, heavy intensity)
                - **71, 73, 75**: Snowfall (Slight, moderate, heavy intensity)
                - **77**: Snow grains
                - **80, 81, 82**: Rain showers (Slight, moderate, violent)
                - **85, 86**: Snow showers (Slight, heavy)
                - **95**: Thunderstorm (Slight or moderate)
                - **96, 99**: Thunderstorm with slight or heavy hail
            """
            )
    else:
        st.error("City not found or weather data unavailable.")
else:
    st.warning("Please enter a city name to get the weather.")
