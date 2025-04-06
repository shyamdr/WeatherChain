# WeatherChain
A Python project to analyze weather impacts on supply chain routes using Open-Meteo API and Spark.

## Features
- Generates random supply chain routes within India (8°N-37°N, 68°E-97°E).
- Fetches weather data (precipitation, wind speed) for route start/end points via Open-Meteo API.
- Caches weather data to reduce API calls.
- Predicts route risk (HIGH/LOW) using Logistic Regression in Spark.
- Saves results to `data/results.parquet` (Parquet format for scalability).

## Setup
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Build the Docker image: `docker build -t weatherchain:latest .`
3. Run via:
   - Windows: `run.bat`
   - VS Code: `Ctrl+Shift+P` > "Tasks: Run Task" > "docker-run"
   - Manual: `docker run -it -v "<your_project_path>:/app" weatherchain:latest`

## Structure
- `src/`:
  - `generate_routes.py`: Creates route CSVs (e.g., `routes_small.csv`).
  - `fetch_weather.py`: Pulls weather data, outputs `weather_results.csv`.
  - `predict_risk.py`: Predicts risks, outputs `results.parquet`.
- `data/`:
  - `routes_small.csv`: Input routes (currently 10).
  - `weather_results.csv`: Weather data per route.
  - `weather_data.csv`: Cached weather grid data.
  - `weather_log.txt`: Process logs.
  - `results.parquet`: Risk predictions.
- Root:
  - `Dockerfile`: Builds the container with Python, Java, Spark.
  - `run.bat`: Runs `predict_risk.py` in Docker.
  - `requirements.txt`: Python dependencies.

## Requirements
- Docker Desktop
- Python 3.11 (in container)
- Spark (via PySpark in container)