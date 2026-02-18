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

### Phase 2: Orchestration (Current)
*   **Goal**: Reliability and automation.
*   **Status**:
    *   [x] Refactored ingestion into Prefect Tasks & Flows (`weather_flow.py`).
    *   [x] Dockerized Prefect environment (ephemeral mode verification).
    *   [ ] **Next**: Set up long-lived Prefect server or Cloud login for observability.

### Phase 3: Data Warehouse (The "Banking" Layer)
*   **Goal**: Structured modeling.
*   **Plan**: Ingest JSON to Databricks Bronze -> dbt to Silver/Gold.

## 📝 Developer Notes
*   **Docker Build**: Run from root: `docker-compose -f docker/docker-compose.yml build`
*   **Docker Run (Orchestration)**: `docker-compose -f docker/docker-compose.yml up`
*   **Governance**: Always ensure we have `schema.yml` for every model (Auditability).

---
## 🛑 Checkpoint: 2026-02-17
**State**: Ingestion Framework & Orchestration Setup Complete.
**Accomplishments**:
1.  **S3 Logic**: Implemented `boto3` logic in `ingest_weather.py` with a `RUN_MODE=local` bypass.
2.  **Environment Restoration**: Rebuilt `docker-compose.yml` to support both raw ingestion and orchestrated flows.
3.  **Phase 2 Start**: Successfully refactored and ran the weather ingestion as a Prefect Flow inside Docker.
4.  **Verification**: Confirmed local simulation of the data lake works via Docker volumes.

**Next Session Start-Up**:
1.  **Run the Flow**: Verify the pipe is still hot:
    ```bash
    docker-compose -f docker/docker-compose.yml up
    ```
2.  **Cloud Transition**: If ready, set up AWS S3 bucket and update `.env` with credentials.
3.  **Orchestration Maturity**: Set up a Prefect schedule or connect to Prefect Cloud for persistent logging.
