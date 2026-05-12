from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="National Voter Management System - Notification Service",
    description="Async notification delivery via Celery + Redis. Email, SMS, In-app.",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    return {"service": "notification_service", "status": "operational"}


@app.get("/health")
def health():
    """Check Celery worker connectivity."""
    from app.workers.tasks import celery_app
    try:
        inspect = celery_app.control.inspect(timeout=1.0)
        stats = inspect.stats()
        workers_online = bool(stats)
    except Exception:
        workers_online = False
    return {"celery_workers_online": workers_online}
