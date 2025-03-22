# WeatherChain
A Python project to analyze weather impacts on supply chain routes using Open-Meteo API and Spark.

## Features
- Fetches weather data (precipitation, wind speed) for route start/end points.
- Processes supply chain routes from CSV.
- Predicts route risk (HIGH/LOW) using Logistic Regression.
- Saves results to `data/results.csv`.

## Setup
1. Install Docker Desktop.
2. Build: `docker build -t weatherchain:latest .`
3. Run: `run.bat` or VS Code task "docker-run".

## Structure
- `src/`: Source scripts.
- `data/`: Input/output CSVs.
- Root: Configs and tools.