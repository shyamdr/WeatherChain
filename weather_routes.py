import requests
import pandas as pd
import time

# Function to get weather for a location
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=UTC"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["daily"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for lat={lat}, lon={lon}: {e}")
        return None

# Load routes
routes = pd.read_csv("routes.csv")

# Prepare results list
results = []

# Loop through routes and fetch weather
for index, row in routes.iterrows():
    start_weather = get_weather(row["start_lat"], row["start_lon"])
    end_weather = get_weather(row["end_lat"], row["end_lon"])
    
    if start_weather is None or end_weather is None:
        print(f"Route {row['route_id']}: Weather data unavailable, skipping.")
        result = {"route_id": row["route_id"], "status": "Skipped", "start_rain": None, "end_rain": None, "risk": None}
        results.append(result)
        continue
    
    start_rain = start_weather["precipitation_sum"][0]
    end_rain = end_weather["precipitation_sum"][int(row["travel_days"]) - 1]
    
    risk = "LOW"
    if start_rain > 10 or end_rain > 10:
        risk = "HIGH"
    
    print(f"Route {row['route_id']}:")
    print(f"  Start (Day 1): {start_rain} mm precipitation")
    print(f"  End (Day {row['travel_days']}): {end_rain} mm precipitation")
    print(f"  Risk: {risk}")
    
    # Store result
    result = {"route_id": row["route_id"], "status": "Processed", "start_rain": start_rain, "end_rain": end_rain, "risk": risk}
    results.append(result)
    
    time.sleep(1)

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("results.csv", index=False)
print("Results saved to results.csv")