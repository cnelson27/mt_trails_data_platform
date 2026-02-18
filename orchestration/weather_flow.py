import requests
import json
import pandas as pd
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError
from prefect import task, flow, get_run_logger

@task(retries=3, retry_delay_seconds=60)
def fetch_weather_data(lat, lon):
    """Fetches weather data from Open-Meteo API."""
    logger = get_run_logger()
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=America%2FDenver"
    
    logger.info(f"Fetching weather data for lat={lat}, lon={lon}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@task
def save_weather_locally(data, folder="data_lake/raw_weather"):
    """Saves weather data to a local JSON file."""
    logger = get_run_logger()
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    # Add ingestion timestamp
    data['ingested_at'] = datetime.now().isoformat()
    
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M')
    file_name = f"billings_weather_{timestamp_str}.json"
    local_path = os.path.join(folder, file_name)
    
    with open(local_path, 'w') as f:
        json.dump(data, f)
    
    logger.info(f"✅ Data saved locally to {local_path}")
    return local_path

@task
def upload_weather_to_s3(local_path, bucket_name):
    """Uploads a file to S3 if configured."""
    logger = get_run_logger()
    run_mode = os.getenv("RUN_MODE", "cloud")
    
    if run_mode == "local":
        logger.info("ℹ️ Running in LOCAL mode. Skipping S3 upload.")
        return None
    
    if not bucket_name:
        logger.warning("⚠️ S3_BUCKET_NAME not set. Skipping S3 upload.")
        return None

    file_name = os.path.basename(local_path)
    s3_key = f"raw/weather/{datetime.now().strftime('%Y/%m/%d')}/{file_name}"
    
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_path, bucket_name, s3_key)
        logger.info(f"🚀 Successfully uploaded to S3: s3://{bucket_name}/{s3_key}")
        return s3_key
    except NoCredentialsError:
        logger.error("❌ AWS credentials not found.")
        raise
    except Exception as e:
        logger.error(f"❌ Error uploading to S3: {e}")
        raise

@flow(name="Weather Ingestion Flow")
def weather_ingestion_flow():
    """Main flow for weather data ingestion."""
    # Billings, MT Coordinates
    lat, lon = 45.7833, -108.5007
    bucket_name = os.getenv("S3_BUCKET_NAME")
    
    data = fetch_weather_data(lat, lon)
    local_path = save_weather_locally(data)
    upload_weather_to_s3(local_path, bucket_name)

if __name__ == "__main__":
    weather_ingestion_flow()
