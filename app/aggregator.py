# app/aggregator.py
import os, asyncio, asyncpg
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lexiadm:lexipwd@postgres:5432/lexidb") # put (postgres) if not locally running
# user: lexiadm
# password: lexipwd
# database: lexidb

async def run_once():
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=2)
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO analytics_hourly (bucket_hour, total_queries, created_at)
            SELECT date_trunc('hour', timestamp) as bucket_hour, count(*) as total_queries, now() as created_at
            FROM events_raw
            WHERE event_type='query' AND timestamp >= now() - interval '1 hour'
            GROUP BY bucket_hour
            ON CONFLICT (bucket_hour) DO UPDATE SET total_queries = EXCLUDED.total_queries, created_at = EXCLUDED.created_at;
        """)
    await pool.close()

if __name__ == "__main__":
    asyncio.run(run_once())
