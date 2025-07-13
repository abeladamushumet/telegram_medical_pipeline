with source as (
    select
        channel_id,
        channel_name,
        min(date::date) as first_message_date,
        max(date::date) as last_message_date,
        count(*) as total_messages
    from {{ ref('stg_telegram_messages') }}
    group by channel_id, channel_name
)

select
    channel_id,
    channel_name,
    first_message_date,
    last_message_date,
    total_messages
from source
