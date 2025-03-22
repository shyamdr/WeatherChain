@echo off
docker run -it -v "D:\Shyam\Side Projects\WeatherChain:/app" weatherchain:latest python /app/src/weather_routes.py