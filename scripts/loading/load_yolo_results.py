import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

# Config
YOLO_RESULTS_DIR = "yolo/results/"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "telegram_dbt",
    "user": "postgres",
    "password": "Abeladamu@7"  
}

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

# Extract image_id from file name
def extract_image_id(image_path):
    try:
        return int(Path(image_path).stem.split("_")[-1])
    except:
        return None

# Load detections
def load_detections():
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO raw.image_detections (image_id, detection_label, confidence, detected_at)
        VALUES (%s, %s, %s, %s)
    """

    for json_file in Path(YOLO_RESULTS_DIR).glob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)

        image_name = data.get("image", "")
        image_id = extract_image_id(image_name)
        detected_at = datetime.now()

        if image_id is None:
            print(f"⚠️ Skipping {json_file.name} (invalid image_id)")
            continue

        for detection in data.get("detections", []):
            label = detection["label"]
            confidence = detection["confidence"]

            cursor.execute(insert_query, (image_id, label, confidence, detected_at))

        print(f"✅ Inserted {len(data['detections'])} detections from {json_file.name}")

    conn.commit()
    cursor.close()
    conn.close()
    print("🎉 All detections loaded successfully.")

if __name__ == "__main__":
    load_detections()
