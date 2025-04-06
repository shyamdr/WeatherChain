from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import logging

logging.basicConfig(filename="/app/data/weather_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", filemode="a")
logger = logging.getLogger()

spark = SparkSession.builder.appName("WeatherChain").getOrCreate()
df = spark.read.csv("/app/data/weather_results.csv", header=True, inferSchema=True)

X_train = [[5, 10], [15, 15], [8, 25], [20, 5], [2, 18], [12, 22], [3, 8], [18, 30], [7, 12], [25, 25]]
y_train = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1]
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

@udf(StringType())
def predict_risk(start_rain, end_rain, start_wind, end_wind):
    rain = max(start_rain or 0, end_rain or 0)
    wind = max(start_wind or 0, end_wind or 0)
    risk = model.predict([[rain, wind]])[0]
    return "HIGH" if risk == 1 else "LOW"

results_df = df.withColumn("risk", predict_risk("start_rain", "end_rain", "start_wind", "end_wind"))
results_df.show(5)
results_df.write.parquet("/app/data/results.parquet", mode="overwrite")
logger.info("Risk prediction complete, results saved to results.parquet")
spark.stop()