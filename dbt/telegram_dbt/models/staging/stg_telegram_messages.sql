with raw as (
    select
        (jsonb ->> 'id')::int as id,
        (jsonb ->> 'date')::timestamp as date,
        (jsonb ->> 'message') as message_text,
        (jsonb ->> 'peer_id')::jsonb ->> 'channel_id' as channel_id,
        case
            when jsonb -> 'media' ->> '@type' = 'messageMediaPhoto' then true
            else false
        end as has_image
    from {{ source('raw', 'telegram_messages') }}
),

cleaned as (
    select
        id,
        date,
        message_text,
        channel_id::int,
        has_image
    from raw
)

select * from cleaned
