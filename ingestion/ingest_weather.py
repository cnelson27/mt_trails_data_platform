import requests
import json
import pandas as pd
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_path, bucket_name, s3_key):
    """Uploads a file to an S3 bucket."""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"🚀 Successfully uploaded to S3: s3://{bucket_name}/{s3_key}")
    except NoCredentialsError:
        print("⚠️ AWS credentials not found. Skipping S3 upload.")
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")

def fetch_billings_trail_weather():
    # Coordinates for Billings, MT
    lat, lon = 45.7833, -108.5007
    
    # API Endpoint for current weather + mountain biking relevant variables
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=America%2FDenver"
    
    print(f"Fetching data for Billings at {datetime.now()}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        
        # Add a timestamp for our "Data Lake" partitioning
        data['ingested_at'] = datetime.now().isoformat()
        
        # Define local landing path (Simulating S3)
        folder = "data_lake/raw_weather"
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M')
        file_name = f"billings_weather_{timestamp_str}.json"
        local_path = os.path.join(folder, file_name)
        
        with open(local_path, 'w') as f:
            json.dump(data, f)
            
        print(f"✅ Success! Data saved locally to {local_path}")

        # --- S3 Upload Logic ---
        bucket_name = os.getenv("S3_BUCKET_NAME")
        run_mode = os.getenv("RUN_MODE", "cloud") # Default to cloud if not specified

        if run_mode == "local":
            print("ℹ️ Running in LOCAL mode. Skipping S3 upload attempt.")
        elif bucket_name:
            s3_key = f"raw/weather/{datetime.now().strftime('%Y/%m/%d')}/{file_name}"
            upload_to_s3(local_path, bucket_name, s3_key)
        else:
            print("⚠️ S3_BUCKET_NAME not set. Define it to enable S3 uploads.")

        return data

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

if __name__ == "__main__":
    fetch_billings_trail_weather()