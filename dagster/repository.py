from dagster import repository
from dagster_pipeline.pipeline import telegram_data_pipeline
from dagster_pipeline import schedule

@repository
def telegram_repo():
    return [telegram_data_pipeline, schedule.daily_telegram_data_pipeline_schedule]
