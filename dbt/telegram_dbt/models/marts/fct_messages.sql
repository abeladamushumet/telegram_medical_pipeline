{{ config(materialized='table') }}

SELECT
    msg.message_id,
    msg.message_date,
    msg.message_text,
    msg.views,
    msg.replies_count,
    msg.post_author,
    msg.grouped_id,
    d.date AS date_key
FROM {{ ref('stg_telegram_messages') }} AS msg
LEFT JOIN {{ ref('dim_dates') }} AS d
    ON msg.message_date::date = d.date
