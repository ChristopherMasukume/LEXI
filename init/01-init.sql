CREATE TABLE IF NOT EXISTS events_raw (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL,
  user_id TEXT,
  session_id TEXT,
  event_type TEXT NOT NULL,
  query_text TEXT,
  query_category TEXT,
  response_time_ms INT,
  model_version TEXT,
  platform TEXT,
  language TEXT,
  session_duration_seconds INT
);

CREATE INDEX IF NOT EXISTS idx_events_ts ON events_raw (timestamp);
CREATE INDEX IF NOT EXISTS idx_events_category ON events_raw (query_category);
CREATE INDEX IF NOT EXISTS idx_events_session ON events_raw (session_id);

CREATE TABLE IF NOT EXISTS analytics_hourly (
  bucket_hour TIMESTAMPTZ PRIMARY KEY,
  total_queries BIGINT,
  created_at TIMESTAMPTZ DEFAULT now()
);
