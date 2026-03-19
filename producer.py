import requests, time, uuid, random, datetime

URL = "http://localhost:8090/ingest"  # matches docker-compose port mapping

categories = ["account","billing","usage","troubleshoot","general"]
platforms = ["web","mobile","api"]

def gen_event():
    sess = str(uuid.uuid4())[:8]
    for _ in range(random.randint(1,5)):
        evt = {
            "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
            "user_id": "anon-"+str(random.randint(1,200)),
            "session_id": sess,
            "event_type": "query",
            "query_text": "sample question about " + random.choice(["login", "account", "billing", "features"]),
            "query_category": random.choice(categories),
            "response_time_ms": random.randint(50,800),
            "model_version": "lexi-v2.3",
            "platform": random.choice(platforms),
            "language": "en"
        }
        yield evt

if __name__ == "__main__":
    while True:
        for e in gen_event():
            try:
                requests.post(URL, json=e, timeout=2)
            except Exception as ex:
                print("err", ex)
        time.sleep(1)

# environment setup: python -m venv venv
# .\venv\Scripts\Activate.ps1
# after running docker-compose, run producer.py to generate sample events through powershell.
# use ID 23942 to access the grafana dashboard at localhost:3000    