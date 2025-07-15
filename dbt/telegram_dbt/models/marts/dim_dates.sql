{{ config(materialized='table') }}

WITH date_range AS (
    SELECT
        generate_series(
            (SELECT MIN(message_date::date) FROM {{ ref('stg_telegram_messages') }}),
            (SELECT MAX(message_date::date) FROM {{ ref('stg_telegram_messages') }}),
            interval '1 day'
        ) AS date
)

SELECT
    date,
    EXTRACT(year FROM date) AS year,
    EXTRACT(month FROM date) AS month,
    EXTRACT(day FROM date) AS day,
    TO_CHAR(date, 'Day') AS day_name,
    EXTRACT(dow FROM date) AS day_of_week
FROM date_range
ORDER BY date
