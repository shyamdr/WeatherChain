# WeatherChain
A Python project to analyze weather impacts on supply chain routes using the Open-Meteo API.

## Features
- Fetches weather data (precipitation, wind speed) for route start/end points.
- Processes a CSV of supply chain routes.
- Predicts route risk (HIGH/LOW) using Logistic Regression based on weather conditions.
- Saves results to `results.csv`.

## Setup
1. Install dependencies: `pip install requests pandas scikit-learn`
2. Run: `python weather_routes.py`