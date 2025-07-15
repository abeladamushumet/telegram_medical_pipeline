from dagster import job

from dagster_pipeline.ops.scrape_ops import scrape_telegram_channels, download_images
from dagster_pipeline.ops.load_ops import load_raw_messages
from dagster_pipeline.ops.transform_ops import run_dbt_transformations
from dagster_pipeline.ops.enrich_ops import run_yolo_enrichment

@job
def telegram_data_pipeline():
    """
    Full end-to-end pipeline:
    - Scrape Telegram data
    - Download images
    - Load to Postgres
    - Transform with dbt
    - Enrich with YOLO
    """
    # Step 1: Scrape messages and download images
    messages_path = scrape_telegram_channels()
    download_images(messages_path)

    # Step 2: Load raw messages to DB
    load_raw_messages(messages_path)

    # Step 3: Run dbt transformations
    run_dbt_transformations()

    # Step 4: Run YOLO enrichment and load results
    run_yolo_enrichment()
