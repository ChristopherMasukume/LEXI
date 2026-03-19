from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os, asyncpg, asyncio

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://lexiadm:lexipwd@postgres:5432/lexidb" # collector DB connection
)

class Event(BaseModel):
    timestamp: datetime
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    event_type: str
    query_text: Optional[str] = None
    query_category: Optional[str] = None
    response_time_ms: Optional[int] = None
    model_version: Optional[str] = None
    platform: Optional[str] = None
    language: Optional[str] = None
    session_duration_seconds: Optional[int] = None

app = FastAPI()
db_pool: Optional[asyncpg.pool.Pool] = None

@app.on_event("startup")
async def startup():
    global db_pool
    for i in range(10):
        try:
            db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
            break
        except Exception as e:
            if i == 9:
                raise
            await asyncio.sleep(1)

@app.on_event("shutdown")
async def shutdown():
    global db_pool
    if db_pool:
        await db_pool.close()

@app.post("/ingest")
async def ingest(evt: Event):
    global db_pool
    if not db_pool:
        raise HTTPException(status_code=500, detail="DB pool not initialized")
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO events_raw (timestamp, user_id, session_id, event_type, query_text,
                                    query_category, response_time_ms, model_version, platform,
                                    language, session_duration_seconds)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
            """,
            evt.timestamp,
            evt.user_id,
            evt.session_id,
            evt.event_type,
            evt.query_text,
            evt.query_category,
            evt.response_time_ms,
            evt.model_version,
            evt.platform,
            evt.language,
            evt.session_duration_seconds
        )
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=False)
