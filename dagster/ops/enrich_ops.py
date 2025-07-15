from dagster import op
import subprocess

@op
def run_yolo_enrichment():
    """
    Runs the YOLO detection script and loads the results into the database.
    """
    print("📸 Running YOLO object detection...")

    try:
        subprocess.run(["python", "yolo/detect_objects.py"], check=True)
        print("✅ YOLO detection complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed during YOLO detection: {e}")
        raise

    print("📥 Loading YOLO results into the database...")

    try:
        subprocess.run(["python", "scripts/loading/load_yolo_results.py"], check=True)
        print("✅ YOLO results loaded into DB.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to load YOLO results into DB: {e}")
        raise
