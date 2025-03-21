# WeatherChain
A Python project to analyze weather impacts on supply chain routes using the Open-Meteo API.

## Features
- Fetches weather data (precipitation, temperature) for route start/end points.
- Processes a CSV of supply chain routes.
- Classifies routes as HIGH or LOW risk based on precipitation (>10mm = HIGH).

## Setup
1. Install dependencies: `pip install requests pandas`
2. Run: `python weather_routes.py`