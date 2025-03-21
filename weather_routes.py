import requests
import pandas as pd
import time

# Function to get weather for a location
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=UTC"
    try:
        response = requests.get(url, timeout=10)  # Set a 10-second timeout
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()["daily"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for lat={lat}, lon={lon}: {e}")
        return None  # Return None if the request fails

# Load routes
routes = pd.read_csv("routes.csv")

# Loop through routes and fetch weather
for index, row in routes.iterrows():
    start_weather = get_weather(row["start_lat"], row["start_lon"])
    end_weather = get_weather(row["end_lat"], row["end_lon"])
    
    # Check if weather data was fetched successfully
    if start_weather is None or end_weather is None:
        print(f"Route {row['route_id']}: Weather data unavailable, skipping.")
        continue
    
    # Get precipitation for start (day 1) and end (arrival day)
    start_rain = start_weather["precipitation_sum"][0]  # Day 1
    end_rain = end_weather["precipitation_sum"][int(row["travel_days"]) - 1]  # Arrival day
    
    print(f"Route {row['route_id']}:")
    print(f"  Start (Day 1): {start_rain} mm precipitation")
    print(f"  End (Day {row['travel_days']}): {end_rain} mm precipitation")
    
    # Add a small delay to avoid overwhelming the API
    time.sleep(1)  # Wait 1 second before the next request