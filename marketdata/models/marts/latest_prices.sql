with base as (
    select * from {{ ref('stg_ohlcv') }}
),

ranked as (
    select
        ticker,
        currency,
        timestamp,
        close,
        volume,
        row_number() over (partition by ticker order by timestamp desc) as rn
    from base
)

select
    ticker,
    currency,
    timestamp as last_updated,
    close as last_price,
    volume as last_volume
from ranked
where rn = 1
