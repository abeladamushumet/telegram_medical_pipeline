from dagster import op
import subprocess

@op
def load_to_postgres():
    """
    Loads raw Telegram message data and image metadata into PostgreSQL.
    """
    print("🗃️ Loading Telegram data into PostgreSQL...")

    try:
        subprocess.run(["python", "scripts/loading/load_to_postgres.py"], check=True)
        print("✅ Telegram data successfully loaded.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to load data into PostgreSQL: {e}")
        raise
