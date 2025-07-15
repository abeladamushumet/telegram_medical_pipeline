with raw_data as (

    select
        message_id,
        date,
        message_text,
        views,
        replies_count,
        post_author,
        photo_sizes,
        grouped_id
    from raw.telegram_messages

)

select
    message_id,
    date::timestamp as message_date,
    coalesce(message_text, '') as message_text,
    coalesce(views, 0) as views,
    coalesce(replies_count, 0) as replies_count,
    post_author,
    -- photo_sizes is JSONB, keep as is or parse if needed
    photo_sizes,
    grouped_id

from raw_data
