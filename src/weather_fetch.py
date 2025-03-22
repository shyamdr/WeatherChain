import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,precipitation_sum&timezone=America/New_York"
response = requests.get(url)
data = response.json()

print(data["daily"])  # See max temp and precipitation for next 7 days