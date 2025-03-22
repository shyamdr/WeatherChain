from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WeatherChain").getOrCreate()
routes_df = spark.read.csv("routes_large.csv", header=True, inferSchema=True)
routes_df.show(5)  # Show first 5 rows
spark.stop()