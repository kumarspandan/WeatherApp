import streamlit as st
import requests

# Function to fetch weather data
def get_weather(city_name, api_key):
    # OpenWeatherMap API URL
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    
    try:
        # Get response from API
        response = requests.get(complete_url)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        
        # Convert response to JSON
        weather_data = response.json()

        # Check if the response contains an error message
        if 'cod' in weather_data and weather_data['cod'] == 200:
            # Extract relevant information
            main_data = weather_data['main']
            weather_desc = weather_data['weather'][0]['description']
            temp = main_data['temp']
            feels_like = main_data['feels_like']
            temp_min = main_data['temp_min']
            temp_max = main_data['temp_max']
            humidity = main_data['humidity']
            pressure = main_data['pressure']
            wind_speed = weather_data['wind']['speed']
            
            return {
                "city": city_name,
                "temperature": temp,
                "feels_like": feels_like,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "humidity": humidity,
                "pressure": pressure,
                "description": weather_desc.capitalize(),
                "wind_speed": wind_speed
            }
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Streamlit app layout
st.set_page_config(page_title="Weather App", page_icon="☀️", layout="centered")

# App title
st.title("🌦️ Real-Time Weather Info")

# Input: City Name
st.write("Enter the name of a city to get current weather information.")
city_name = st.text_input("City Name", "")

# Button to get weather data
if st.button("Get Weather"):
    if city_name:
        # Fetch the weather data using the secret api_key
        api_key = st.secrets["api_key"]  # Fetch API key from Streamlit Secrets
        weather_info = get_weather(city_name, api_key)
        
        # Display the result
        if weather_info:
            st.subheader(f"🌍 Weather in **{weather_info['city'].capitalize()}**")

            # Format output as paragraphs
            output = (
                f"🌡️ Temperature: {weather_info['temperature']}°C, "
                f"😌 Feels Like: {weather_info['feels_like']}°C, "
                f"🌡️ Min Temperature: {weather_info['temp_min']}°C\n\n"
                
                f"**🌡️ Max Temperature:** {weather_info['temp_max']}°C, "
                f"**💧 Humidity:** {weather_info['humidity']}%, "
                f"**🌬️ Wind Speed:** {weather_info['wind_speed']} m/s\n\n"
                
                f"**🌬️ Pressure:** {weather_info['pressure']} hPa, "
                f"**☁️ Description:** {weather_info['description']}."
            )

            # Display the formatted output with color and font style
            st.markdown(f"<p style='font-family: sans-serif; color: #4A90E2;'>{output}</p>", unsafe_allow_html=True)
        else:
            st.error(f"Could not find weather data for '{city_name}'. Please check the city name and try again.")
    else:
        st.warning("Please enter a city name.")

# Styling for the button
st.markdown("""
    <style>
        div.stButton > button { 
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
        }
    </style>
""", unsafe_allow_html=True)
