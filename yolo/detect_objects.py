import os
from pathlib import Path
import torch
import json
from ultralytics import YOLO

# Config
MODEL_PATH = "yolov8n.pt"  
IMAGES_DIR = Path("data/images/")
OUTPUT_DIR = Path("yolo/results/")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def detect_objects():
    # Load the YOLO model
    model = YOLO(MODEL_PATH)

    results_summary = []

    # Traverse all subfolders and get .jpg, .jpeg, .png files
    image_files = list(IMAGES_DIR.rglob("*.jpg")) + list(IMAGES_DIR.rglob("*.jpeg")) + list(IMAGES_DIR.rglob("*.png"))

    if not image_files:
        print("❌ No images found in data/images/ or subfolders.")
        return

    for image_file in image_files:
        print(f"📷 Processing: {image_file}")

        try:
            # Run detection
            results = model(image_file)
        except Exception as e:
            print(f"⚠️ Skipping {image_file} due to error: {e}")
            continue

        preds = results[0]
        detections = []

        # Loop over each detection box
        for box, conf, cls in zip(preds.boxes.xyxy, preds.boxes.conf, preds.boxes.cls):
            bbox = box.cpu().numpy().tolist()
            confidence = float(conf.cpu())
            class_id = int(cls.cpu())
            label = model.names[class_id]

            detections.append({
                "bbox": bbox,
                "confidence": confidence,
                "label": label
            })

        # Save results to JSON
        output_path = OUTPUT_DIR / f"{image_file.stem}_detections.json"
        with open(output_path, "w") as f:
            json.dump({
                "image": str(image_file),
                "detections": detections
            }, f, indent=2)

        results_summary.append({
            "image": str(image_file),
            "detections_count": len(detections),
            "output_file": str(output_path)
        })

    print("\n✅ Detection complete.")
    for res in results_summary:
        print(f"✔️ {res['image']}: {res['detections_count']} objects → {res['output_file']}")

if __name__ == "__main__":
    detect_objects()
