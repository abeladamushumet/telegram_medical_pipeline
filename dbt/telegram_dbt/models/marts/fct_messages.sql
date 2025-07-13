with base as (
    select
        msg.id as message_id,
        msg.channel_id,
        cast(date_trunc('day', msg.date) as date) as date_day,
        msg.message_text,
        msg.has_image,
        length(coalesce(msg.message_text, '')) as message_length
    from {{ ref('stg_telegram_messages') }} msg
),

final as (
    select
        message_id,
        channel_id,
        date_day,
        message_text,
        has_image,
        message_length
    from base
)

select * from final
