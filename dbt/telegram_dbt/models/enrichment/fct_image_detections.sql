with detections as (

    select
        message_id,
        detected_object_class,
        confidence_score
    from {{ source('raw', 'image_detections') }}

),

final as (

    select
        message_id,
        detected_object_class,
        confidence_score
    from detections
    where confidence_score >= 0.3  -- filter out low-confidence predictions

)

select * from final
