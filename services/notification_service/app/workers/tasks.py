"""
Notification Celery tasks.
All delivery is async and retryable — no blocking calls in API routes.

Channels implemented:
  - Email (via SMTP / SendGrid)
  - SMS (via Twilio / Msg91)
  - In-app (persisted to DB)

Queues:
  - notifications.email    (concurrency=4)
  - notifications.sms      (concurrency=8)
  - notifications.inapp    (concurrency=2)
"""
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# ── Celery app ────────────────────────────────────────────────────────────────
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("notifications", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=120,
    task_acks_late=True,                   # only ack after success (at-least-once)
    task_reject_on_worker_lost=True,
    task_routes={
        "tasks.send_email": {"queue": "notifications.email"},
        "tasks.send_sms": {"queue": "notifications.sms"},
        "tasks.send_inapp": {"queue": "notifications.inapp"},
    },
)


# ── Email task ────────────────────────────────────────────────────────────────
@celery_app.task(bind=True, name="tasks.send_email", max_retries=3, default_retry_delay=60)
def send_email(self, to: str, subject: str, body_html: str, body_text: str = ""):
    """
    Send email via SMTP.
    In production configure SMTP_HOST, SMTP_USER, SMTP_PASS env vars.
    """
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    from_addr = os.getenv("SMTP_FROM", "noreply@voterportal.gov.in")

    if not smtp_user:
        logger.warning("SMTP_USER not set — email queued but not dispatched (dev mode)")
        return {"status": "dev_skip", "to": to, "subject": subject}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to
    if body_text:
        msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_addr, [to], msg.as_string())
        logger.info("Email sent to %s — %s", to, subject)
        return {"status": "sent", "to": to}
    except Exception as exc:
        logger.error("Email delivery failed: %s", exc)
        raise self.retry(exc=exc)


# ── SMS task ──────────────────────────────────────────────────────────────────
@celery_app.task(bind=True, name="tasks.send_sms", max_retries=3, default_retry_delay=30)
def send_sms(self, phone: str, message: str):
    """
    Send SMS via Twilio or Msg91.
    Configure TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM env vars.
    """
    twilio_sid = os.getenv("TWILIO_SID", "")
    twilio_token = os.getenv("TWILIO_TOKEN", "")
    twilio_from = os.getenv("TWILIO_FROM", "")

    if not twilio_sid:
        logger.warning("Twilio not configured — SMS queued but not dispatched (dev mode)")
        return {"status": "dev_skip", "phone": phone}

    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        client.messages.create(body=message, from_=twilio_from, to=phone)
        logger.info("SMS sent to %s", phone)
        return {"status": "sent", "phone": phone}
    except Exception as exc:
        logger.error("SMS delivery failed: %s", exc)
        raise self.retry(exc=exc)


# ── In-app notification task ───────────────────────────────────────────────────
@celery_app.task(bind=True, name="tasks.send_inapp", max_retries=2)
def send_inapp(self, user_id: str, title: str, body: str, category: str = "general"):
    """
    Persist an in-app notification to Supabase Realtime channel.
    """
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    if not supabase_url:
        logger.warning("Supabase not configured — in-app notification skipped")
        return {"status": "dev_skip"}

    try:
        import httpx
        resp = httpx.post(
            f"{supabase_url}/rest/v1/notifications",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
            },
            json={"user_id": user_id, "title": title, "body": body, "category": category, "is_read": False},
            timeout=10,
        )
        resp.raise_for_status()
        return {"status": "sent", "user_id": user_id}
    except Exception as exc:
        logger.error("In-app notification failed: %s", exc)
        raise self.retry(exc=exc)
