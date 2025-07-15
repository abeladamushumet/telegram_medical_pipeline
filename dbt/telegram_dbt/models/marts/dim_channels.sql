{{ config(materialized='table') }}

SELECT DISTINCT
    post_author AS channel_name
FROM {{ ref('stg_telegram_messages') }}
WHERE post_author IS NOT NULL
