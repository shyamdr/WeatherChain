FROM python:3.11
WORKDIR /app
# Install Java
RUN apt-get update && apt-get install -y openjdk-17-jre-headless && apt-get clean
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Install Python deps
RUN pip install pandas requests scikit-learn numpy pyspark
COPY . /app
CMD ["python", "src/predict_risk.py"]