import requests
import pandas as pd
import logging
import os

logging.basicConfig(filename="/app/data/weather_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", filemode="w")
logger = logging.getLogger()

def get_weather(lat, lon):
    grid_lat = round(lat * 2) / 2
    grid_lon = round(lon * 2) / 2
    key = f"{grid_lat},{grid_lon}"
    cache_file = "/app/data/weather_data.csv"
    if os.path.exists(cache_file):
        cache_df = pd.read_csv(cache_file)
        if key in cache_df["key"].values:
            row = cache_df[cache_df["key"] == key].iloc[0]
            logger.info(f"Cache hit for {key}")
            return (row["rain"], row["wind"])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={grid_lat}&longitude={grid_lon}&daily=precipitation_sum,windspeed_10m_max&timezone=UTC"
    logger.info(f"Fetching weather for {key}")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()["daily"]
        rain, wind = data["precipitation_sum"][0], data["windspeed_10m_max"][0]
        pd.DataFrame([{"key": key, "rain": rain, "wind": wind}]).to_csv(cache_file, mode="a", header=not os.path.exists(cache_file), index=False)
        return (rain, wind)
    except:
        logger.info(f"Error fetching {key}")
        return (None, None)

routes = pd.read_csv("/app/data/routes_small.csv")
weather_data = []
for _, row in routes.iterrows():
    start_weather = get_weather(row["start_lat"], row["start_lon"])
    end_weather = get_weather(row["end_lat"], row["end_lon"])
    weather_data.append({
        "route_id": row["route_id"],
        "start_rain": start_weather[0],
        "start_wind": start_weather[1],
        "end_rain": end_weather[0],
        "end_wind": end_weather[1]
    })
pd.DataFrame(weather_data).to_csv("/app/data/weather_results.csv", index=False)
logger.info("Weather data saved to data/weather_results.csv")