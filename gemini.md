# Montana Trail & Recreation Platform - Project Context

## 🎯 Project Vision
**"Banking for Trails"**: A data engineering portfolio project that applies rigorous data governance (mimicking banking standards) to outdoor recreation data.
**Hypothetical Use Case**: A "Billings Outdoor Impact Dashboard" used to evaluate community investment based on trail usage and volunteer activity.

## � Learning Goal
**Focus**: Master the tools step-by-step. Do not rush.
**Current Lesson**: Docker basics (Build Contexts, Image Layering) & Project Directory structure.

## �🏗️ Architecture & Stack
*   **Infrastructure**: AWS Free Tier (S3 for Data Lake).
*   **Ingestion**: Python (Requests, Pandas) running in Docker containers.
*   **Orchestration**: Prefect Cloud (or Airflow) for scheduling and retries.
*   **Transformation**: dbt Core (Medallion Architecture: Bronze/Silver/Gold).
*   **Warehouse**: Databricks Community Edition (Delta Lake).
*   **Visualization**: Apache Superset or Sigma Computing.

## 📂 Directory Structure Strategy
*   `ingestion/`: Raw scripts. Docker build context is **Root**.
*   `docker/`: Container definitions. Run builds from **Root** pointing here.
*   `data_lake/`: Local simulation of S3 bucket (git-ignored).
*   `dbt_project/`: Transformation logic (Schema tests are critical).

## 📅 Roadmap & Status

### Phase 1: Ingestion Framework (Current)
*   **Goal**: Dockerized API ingestion to S3.
*   **Status**:
    *   [x] `ingest_weather.py`: Fetches Open-Meteo data for Billings + S3 logic.
    *   [x] `Dockerfile`: Multi-stage build (Python 3.11).
    *   [x] `docker-compose`: Local execution mounting `data_lake/`.
    *   [ ] **Next**: Transition to **Cloud**: Set up AWS S3 bucket and credentials.

### Phase 2: Orchestration
*   **Goal**: Reliability and automation.
*   **Plan**: Wrap ingestion in a Prefect Flow (`weather_flow.py`).

### Phase 3: Data Warehouse (The "Banking" Layer)
*   **Goal**: Structured modeling.
*   **Plan**: Ingest JSON to Databricks Bronze -> dbt to Silver/Gold.

## 📝 Developer Notes
*   **Docker Build**: Run from root: `docker build -t mt-trails -f docker/Dockerfile .`
*   **Docker Run**: `docker-compose -f docker/docker-compose.yml up`
*   **Governance**: Always ensure we have `schema.yml` for every model (Auditability).

---
## 🛑 Checkpoint: 2026-02-03
**State**: Docker Image Successfully Built.
**Accomplishments**:
1.  Created generic `ingest_weather.py` for Billings data.
2.  Restructured project to separate `ingestion/` and `docker/` logic.
3.  **Learned**: "Build Context". Use `docker build -f docker/Dockerfile .` (run from root) to ensure the Dockerfile can see files in `ingestion/`.
4.  **Issue Resolved**: Added Docker to Windows PATH.

**Next Session Start-Up**:
1.  Run the container to verify it produces data:
    ```bash
    docker-compose -f docker/docker-compose.yml up --build
    ```
2.  Check `data_lake/raw_weather/` for the new `.json` file.
3.  Transition to **Cloud**: Set up AWS S3 bucket and credentials.
