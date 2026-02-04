# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ingestion/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create the data lake directory inside the container
# RUN mkdir -p data_lake/raw_weather

# Run the ingestion script when the container launches
CMD ["python", "ingestion/ingest_weather.py"]
