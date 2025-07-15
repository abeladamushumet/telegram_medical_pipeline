from dagster import schedule
from dagster_pipeline.pipeline import telegram_data_pipeline

@schedule(
    cron_schedule="0 7 * * *",  # Every day at 07:00 AM
    pipeline_name="telegram_data_pipeline",
    execution_timezone="Africa/Addis_Ababa"  # Set to your timezone if needed
)
def daily_telegram_data_pipeline_schedule(_context):
    return {}

