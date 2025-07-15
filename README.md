# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Overview

This project delivers a full ELT (Extract → Load → Transform) pipeline for analyzing public Ethiopian medical Telegram channels. The system scrapes messages and media, processes them, enriches them using object detection, and serves insights via an API—all orchestrated using Dagster.

Built for Kara Solutions, this pipeline supports better understanding of medicine promotions, pricing, and trends via Telegram.

---

## Tech Stack

| Layer           | Tool/Library     | Purpose                             |
|----------------|------------------|-------------------------------------|
| Extraction      | Telethon         | Telegram scraping                   |
| Storage         | PostgreSQL       | Data warehouse                      |
| Transformation  | dbt              | Star schema modeling, tests         |
| Enrichment      | YOLOv8 (Ultralytics) | Image object detection         |
| API             | FastAPI + Pydantic| Insightful, structured API         |
| Orchestration   | Dagster          | Schedule and monitor pipeline       |
| Deployment      | Docker + .env    | Reproducible, secure setup          |

---

## Architecture

```text
┌──────────────┐     ┌─────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
| Telegram API | --> | Raw DataLake| --> | PostgreSQL | --> | dbt Models | --> | FastAPI     |
└──────────────┘     └─────────────┘     └────────────┘     └────────────┘     └────────────┘
                                                            ↘
                                                             YOLOv8 Enrichment
```

---

## Features

- Scrapes structured + unstructured Telegram content (text, images)
- Stores raw JSON by date and channel in a data lake
- Loads into PostgreSQL with schema
- Cleans and transforms with dbt (star schema: facts + dimensions)
- Detects objects (e.g., pills, creams) using YOLOv8
- Serves analytics via RESTful FastAPI
- Fully orchestrated via Dagster with scheduling
- Includes EDA notebook for visualization
- Containerized with Docker for reproducibility

---

## YOLOv8 Enrichment

- Uses Ultralytics YOLOv8 model to analyze image posts
- Detects objects like pills, bottles, creams
- Extracts: `label`, `confidence_score`, and `bounding_box`
- Saves enriched results in `fct_image_detections`
- Links image detections to text messages via `message_id`

Run it with:
```bash
python scripts/yolo_enrichment/run_yolo.py
```

---

## FastAPI Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/reports/top-products?limit=10` | Get top mentioned medical products |
| `/api/channels/{channel_name}/activity` | Message count per day for a channel |
| `/api/search/messages?query=paracetamol` | Full-text search for medical terms |

Launch server:
```bash
uvicorn api.main:app --reload
```
Visit Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Dagster Orchestration

- Uses `@op` for modular pipeline tasks:
  - `scrape_telegram_data`
  - `load_to_postgres`
  - `run_dbt`
  - `run_yolo_enrichment`
- Connected using a `@job`
- Scheduled using `@schedule` to run daily
- Launched locally with:
```bash
dagster dev
```
View Dagit UI at: [http://localhost:3000](http://localhost:3000)

---

## Visual Insights (in `notebooks/eda.ipynb`)

- Daily message volumes
- Object detection trends
- Top active channels
- Label distribution of detected objects

---

## Authors & Mentors

- Built by Abel Adamu Shumet
- Mentored by Mahlet, Rediet, Kerod, Rehmet @10Academy

---

## Acknowledgements

- [Ultralytics](https://github.com/ultralytics/ultralytics)
- [dbt Labs](https://www.getdbt.com/)
- [Dagster](https://dagster.io/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

> "From messy Telegram messages to actionable medical insights – we shipped a data product!" 

