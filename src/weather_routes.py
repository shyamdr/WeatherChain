from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StructType, StructField, FloatType, StringType
import requests
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(filename="/app/data/weather_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", filemode="w")
logger = logging.getLogger()

# Weather fetch with file caching
cache_file = "/app/data/weather_data.csv"
def get_weather(lat, lon, call_count):
    grid_lat = round(lat * 2) / 2  # Snap to 0.5°
    grid_lon = round(lon * 2) / 2
    key = f"{grid_lat},{grid_lon}"
    if os.path.exists(cache_file):
        cache_df = pd.read_csv(cache_file)
        if key in cache_df["key"].values:
            row = cache_df[cache_df["key"] == key].iloc[0]
            logger.info(f"Cache hit for {key}")
            return (row["rain"], row["wind"])
    if call_count[0] >= 10:  # Cap at 10 calls
        logger.info(f"API limit reached, faking {key}")
        return fake_weather(grid_lat, grid_lon)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={grid_lat}&longitude={grid_lon}&daily=precipitation_sum,windspeed_10m_max&timezone=UTC"
    try:
        logger.info(f"Fetching weather for {key}")
        response = requests.get(url, timeout=10)
        data = response.json()["daily"]
        rain, wind = data["precipitation_sum"][0], data["windspeed_10m_max"][0]
        pd.DataFrame([{"key": key, "rain": rain, "wind": wind}]).to_csv(cache_file, mode="a", header=not os.path.exists(cache_file), index=False)
        call_count[0] += 1
        return (rain, wind)
    except:
        logger.info(f"Error fetching {key}, faking")
        return fake_weather(grid_lat, grid_lon)

# Fake weather for India
def fake_weather(lat, lon):
    if lat < 15 and lon > 75:  # Coastal
        return (np.random.uniform(5, 20), np.random.uniform(5, 15))
    elif lat > 30:  # North
        return (np.random.uniform(0, 5), np.random.uniform(10, 25))
    else:  # Central
        return (np.random.uniform(0, 10), np.random.uniform(5, 20))

# Spark setup
spark = SparkSession.builder.appName("WeatherChain").getOrCreate()
routes_df = spark.read.csv("/app/data/routes_large.csv", header=True, inferSchema=True)

# Weather UDF with call counter
call_count = [0]
weather_udf = udf(lambda lat, lon: get_weather(lat, lon, call_count), 
                 StructType([StructField("rain", FloatType()), StructField("wind", FloatType())]))

# Process routes
routes_with_weather = routes_df.withColumn("start_weather", weather_udf("start_lat", "start_lon")) \
                               .withColumn("end_weather", weather_udf("end_lat", "end_lon"))
routes_processed = routes_with_weather.select(
    "route_id",
    col("start_weather.rain").alias("start_rain"),
    col("start_weather.wind").alias("start_wind"),
    col("end_weather.rain").alias("end_rain"),
    col("end_weather.wind").alias("end_wind")
)

# Predict risk
pandas_df = routes_processed.toPandas()
X_train = np.array([[5, 10], [15, 15], [8, 25], [20, 5], [2, 18], [12, 22], [3, 8], [18, 30], [7, 12], [25, 25]])
y_train = np.array([0, 1, 1, 1, 0, 1, 0, 1, 0, 1])
model = LogisticRegression()
model.fit(X_train, y_train)
pandas_df["risk"] = pandas_df.apply(
    lambda row: "HIGH" if model.predict([[max(row["start_rain"] or 0, row["end_rain"] or 0), 
                                           max(row["start_wind"] or 0, row["end_wind"] or 0)]])[0] == 1 else "LOW",
    axis=1
)
results_df = spark.createDataFrame(pandas_df)
results_df.write.csv("/app/data/results.csv", header=True, mode="overwrite")

# Show results
results_df.show(5)
logger.info(f"Total API calls made: {call_count[0]}")
spark.stop()