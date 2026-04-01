with source as (
    select * from MARKETDATA.RAW.OHLCV
),

deduped as (
    select
        timestamp,
        ticker,
        open,
        high,
        low,
        close,
        volume,
        currency,
        ingested_at,
        row_number() over (
            partition by timestamp, ticker
            order by ingested_at desc
        ) as row_num
    from source
)

select
    timestamp,
    ticker,
    open,
    high,
    low,
    close,
    volume,
    currency,
    ingested_at
from deduped
where row_num = 1
