import requests
import pandas as pd
import time
from sklearn.linear_model import LogisticRegression
import numpy as np

# Function to get weather for a location
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum,windspeed_10m_max&timezone=UTC"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["daily"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for lat={lat}, lon={lon}: {e}")
        return None

# Synthetic training data (rain, wind -> risk)
X_train = np.array([
    [5, 10], [15, 15], [8, 25], [20, 5], [2, 18],  # [rain, wind]
    [12, 22], [3, 8], [18, 30], [7, 12], [25, 25]
])
y_train = np.array([0, 1, 1, 1, 0, 1, 0, 1, 0, 1])  # 0 = LOW, 1 = HIGH

# Train a simple model
model = LogisticRegression()
model.fit(X_train, y_train)

# Load routes
routes = pd.read_csv("routes.csv")
results = []

# Loop through routes and fetch weather
for index, row in routes.iterrows():
    start_weather = get_weather(row["start_lat"], row["start_lon"])
    end_weather = get_weather(row["end_lat"], row["end_lon"])
    
    if start_weather is None or end_weather is None:
        print(f"Route {row['route_id']}: Weather data unavailable, skipping.")
        result = {"route_id": row["route_id"], "status": "Skipped", "start_rain": None, "end_rain": None, "start_wind": None, "end_wind": None, "risk": None}
        results.append(result)
        continue
    
    start_rain = start_weather["precipitation_sum"][0]
    end_rain = end_weather["precipitation_sum"][int(row["travel_days"]) - 1]
    start_wind = start_weather["windspeed_10m_max"][0]
    end_wind = end_weather["windspeed_10m_max"][int(row["travel_days"]) - 1]
    
    # Predict risk with ML (using max of start/end for simplicity)
    features = [[max(start_rain, end_rain), max(start_wind, end_wind)]]
    risk_pred = model.predict(features)[0]
    risk = "HIGH" if risk_pred == 1 else "LOW"
    
    print(f"Route {row['route_id']}:")
    print(f"  Start (Day 1): {start_rain} mm precipitation, {start_wind} m/s wind")
    print(f"  End (Day {row['travel_days']}): {end_rain} mm precipitation, {end_wind} m/s wind")
    print(f"  Risk: {risk}")
    
    result = {"route_id": row["route_id"], "status": "Processed", "start_rain": start_rain, "end_rain": end_rain, "start_wind": start_wind, "end_wind": end_wind, "risk": risk}
    results.append(result)
    
    time.sleep(1)

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("results.csv", index=False)
print("Results saved to results.csv")