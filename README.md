# Montana Trail & Recreation Platform

A data engineering portfolio project mimicking a real-world data ecosystem. This project balances "plumbing" (infrastructure) and "logic" (data modeling), structured around a **Medallion Architecture** for trail conditions and outdoor volunteer events in Billings, MT.

## 🏗️ Tech Stack (Low-Cost / Free Tier)

*   **Cloud Infrastructure:** AWS Free Tier (S3 object storage)
*   **Ingestion:** Python (Containerized with Docker)
*   **Orchestration:** Prefect Cloud / Airflow
*   **Data Warehouse:** Databricks Community Edition
*   **Transformation:** dbt Core
*   **BI & Visualization:** Apache Superset / Sigma Computing

## 🗺️ Roadmap & Phases

### 📈 Phase 1: The "Silver Bow" Ingestion Pipeline
**Goal:** Learn API ingestion, Docker, and Cloud Storage.
*   [x] **Scripting**: Python script to pull Billings weather data (`ingest_weather.py`).
*   [ ] **Containerization**: Dockerize the script.
*   [ ] **Storage**: Push raw JSON logic to AWS S3 (Landing Zone).

### 🔄 Phase 2: Orchestration
**Goal:** Schedule, monitor, and handle pipeline failures.
*   [ ] Automate Phase 1 script to run daily (e.g., 6 AM).
*   [ ] Implement retries and alerts (Slack/Email).

### 🏗️ Phase 3: The Databricks Lakehouse & dbt
**Goal:** "Banking for Trails" - Data modeling and SQL engineering.
*   **Bronze**: Raw JSON/CSV in Databricks.
*   **Silver**: Cleaned tables, filtered for Billings-area trails.
*   **Gold**: High-level business tables (e.g., `fact_trail_usage`, `dim_volunteer_activity`).
*   **Governance**: `schema.yml` documentation and data quality tests.

### 📊 Phase 4: Visualization
**Goal:** End-user value ("Billings Outdoor Impact Dashboard").
*   [ ] Map-based dashboard: Trail density vs. volunteer activity.

## 📂 Project Structure

```text
mt_trails_data_platform/
├── data_lake/          # Local landing zone for raw data
├── ingestion/          # Python scripts for API data fetching
├── dags/               # Orchestration workflows (Airflow/Prefect)
├── dbt_project/        # dbt models and schema tests
├── tests/              # Unit and integration tests
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```
