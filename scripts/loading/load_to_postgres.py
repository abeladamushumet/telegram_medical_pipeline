import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB", "telegram_dbt")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Abeladamu@7")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

RAW_DATA_DIR = "data/raw/telegram_messages"
TARGET_TABLE = "raw.telegram_messages"

def load_json_to_postgres(filepath, conn):
    with open(filepath, "r", encoding="utf-8") as f:
        messages = json.load(f)

    if not messages:
        print(f"[EMPTY] No messages found in {filepath}")
        return

    rows = []
    for msg in messages:
        replies = msg.get("replies")
        replies_count = replies.get("replies") if isinstance(replies, dict) else None

        media = msg.get("media")
        photo_sizes = None
        if isinstance(media, dict):
            photo = media.get("photo")
            if isinstance(photo, dict):
                photo_sizes = photo.get("sizes", [])

        rows.append((
            msg.get("id"),
            msg.get("date"),
            msg.get("message"),
            msg.get("views"),
            replies_count,
            msg.get("post_author"),
            json.dumps(photo_sizes) if photo_sizes else None,  # Serialize only if exists
            msg.get("grouped_id")
        ))

    insert_query = f"""
        INSERT INTO {TARGET_TABLE} (
            message_id, date, message_text, views, replies_count,
            post_author, photo_sizes, grouped_id
        )
        VALUES %s
        ON CONFLICT (message_id) DO NOTHING;
    """

    with conn.cursor() as cur:
        execute_values(cur, insert_query, rows)
        conn.commit()
        print(f"[LOADED] {len(rows)} records from {filepath}")

def main():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("[DB CONNECTED]")

        for root, _, files in os.walk(RAW_DATA_DIR):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    print(f"[PROCESSING] Loading data from {filepath}")
                    load_json_to_postgres(filepath, conn)

        conn.close()
        print("[DONE] All data loaded successfully.")

    except Exception as e:
        print(f"[ERROR] Database connection or loading failed: {e}")

if __name__ == "__main__":
    main()
