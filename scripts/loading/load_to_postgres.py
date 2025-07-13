import os
import json
import psycopg2
from dotenv import load_dotenv
from scripts.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Load env vars
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

RAW_DATA_DIR = "data/raw/telegram_messages"

def load_json_file_to_postgres(filepath, cursor, channel_name):
    logger.info(f"Loading: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        try:
            cursor.execute("""
                INSERT INTO raw_telegram_messages (channel, message_id, message_data)
                VALUES (%s, %s, %s)
                ON CONFLICT (channel, message_id) DO NOTHING
            """, (
                channel_name,
                msg.get("id"),
                json.dumps(msg)
            ))
        except Exception as e:
            logger.error(f"Error inserting message {msg.get('id')} from {channel_name}: {e}")

def main():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        logger.info("Connected to PostgreSQL database")

        for root, _, files in os.walk(RAW_DATA_DIR):
            for file in files:
                if file.endswith(".json"):
                    channel_name = os.path.splitext(file)[0]
                    filepath = os.path.join(root, file)
                    load_json_file_to_postgres(filepath, cursor, channel_name)

        conn.commit()
        logger.info("All data committed successfully")

    except Exception as e:
        logger.error(f"Database connection or loading failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    main()