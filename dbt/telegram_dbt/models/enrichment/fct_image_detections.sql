{{ config(materialized='table') }}

SELECT
    id AS message_id,
    image_id,
    detection_label AS label,
    confidence,
    detected_at
FROM {{ source('raw', 'image_detections') }}
