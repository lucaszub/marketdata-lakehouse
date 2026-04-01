with base as (
    select * from {{ ref('stg_ohlcv') }}
)

select
    date_trunc('day', timestamp) as date,
    ticker,
    currency,
    min(open)  as open,
    max(high)  as high,
    min(low)   as low,
    last_value(close) over (
        partition by date_trunc('day', timestamp), ticker
        order by timestamp
        rows between unbounded preceding and unbounded following
    ) as close,
    sum(volume) as volume
from base
group by 1, 2, 3, close, timestamp
qualify row_number() over (
    partition by date_trunc('day', timestamp), ticker
    order by timestamp desc
) = 1
