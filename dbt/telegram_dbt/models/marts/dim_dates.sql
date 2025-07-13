with distinct_dates as (
    select distinct
        cast(date_trunc('day', date) as date) as date_day
    from {{ ref('stg_telegram_messages') }}
),

dates as (
    select
        date_day,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        extract(day from date_day) as day,
        extract(dow from date_day) as day_of_week,  -- Sunday = 0
        to_char(date_day, 'Day') as day_name,
        to_char(date_day, 'Month') as month_name,
        extract(week from date_day) as week_of_year,
        date_day = current_date as is_today
    from distinct_dates
)

select * from dates
order by date_day
