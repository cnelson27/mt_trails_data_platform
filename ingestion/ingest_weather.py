import requests
import json
import pandas as pd
from datetime import datetime
import os

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
            os.makedirs(folder)
            
        file_name = f"{folder}/billings_weather_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        with open(file_name, 'w') as f:
            json.dump(data, f)
            
        print(f"✅ Success! Data saved to {file_name}")
        return data

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

if __name__ == "__main__":
    fetch_billings_trail_weather()