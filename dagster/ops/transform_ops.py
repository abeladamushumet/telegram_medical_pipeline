from dagster import op
import subprocess

@op
def run_dbt_transformations():
    """
    Executes dbt models to transform and structure the loaded data.
    """
    print("🧪 Running dbt models...")

    try:
        subprocess.run(["dbt", "run", "--project-dir", "dbt/telegram_dbt", "--profile", "telegram_dbt_profile"], check=True)
        print("✅ dbt models ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ dbt run failed: {e}")
        raise
