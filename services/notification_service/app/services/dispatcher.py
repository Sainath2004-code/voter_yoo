"""
Notification dispatcher — called by other services to fire notifications.
Enqueues Celery tasks without blocking the caller.
"""
from app.workers.tasks import send_email, send_sms, send_inapp


class NotificationDispatcher:
    """High-level API consumed by voter_service, election_service etc."""

    # ── Voter Registration events ─────────────────────────────────────────────

    @staticmethod
    def voter_application_submitted(email: str, phone: str, user_id: str, application_id: str):
        send_email.apply_async(
            kwargs={
                "to": email,
                "subject": "Your Voter Registration Application Has Been Received",
                "body_html": f"""
                <h2>Application Received</h2>
                <p>Your Form 6 application has been submitted successfully.</p>
                <p><strong>Application ID:</strong> {application_id}</p>
                <p>A Booth Level Officer will contact you for verification within 5 working days.</p>
                """,
            },
            queue="notifications.email",
        )
        send_sms.apply_async(
            kwargs={
                "phone": phone,
                "message": f"Your voter registration application {application_id} has been received. Track status on the National Voter Portal.",
            },
            queue="notifications.sms",
        )
        send_inapp.apply_async(
            kwargs={
                "user_id": user_id,
                "title": "Application Submitted",
                "body": f"Your Form 6 application ({application_id}) is under review.",
                "category": "voter_registration",
            },
            queue="notifications.inapp",
        )

    @staticmethod
    def application_approved(email: str, phone: str, user_id: str, epic_number: str):
        send_email.apply_async(
            kwargs={
                "to": email,
                "subject": "Your Voter ID (EPIC) Has Been Issued!",
                "body_html": f"""
                <h2>Congratulations! You are a Registered Voter</h2>
                <p>Your Voter ID Card (EPIC) has been generated.</p>
                <p><strong>EPIC Number:</strong> {epic_number}</p>
                <p>Download your EPIC from the National Voter Portal.</p>
                """,
            },
            queue="notifications.email",
        )
        send_sms.apply_async(
            kwargs={
                "phone": phone,
                "message": f"Congratulations! Your Voter ID (EPIC: {epic_number}) has been issued. Download it on the National Voter Portal.",
            },
            queue="notifications.sms",
        )
        send_inapp.apply_async(
            kwargs={
                "user_id": user_id,
                "title": "EPIC Issued",
                "body": f"Your Voter ID {epic_number} is ready for download.",
                "category": "voter_registration",
            },
            queue="notifications.inapp",
        )

    @staticmethod
    def grievance_assigned(email: str, user_id: str, grievance_id: str, officer_name: str):
        send_inapp.apply_async(
            kwargs={
                "user_id": user_id,
                "title": "Grievance Assigned",
                "body": f"Your grievance {grievance_id} has been assigned to {officer_name} for investigation.",
                "category": "grievance",
            },
            queue="notifications.inapp",
        )

    @staticmethod
    def election_phase_announced(email: str, user_id: str, phase: str, date: str):
        send_email.apply_async(
            kwargs={
                "to": email,
                "subject": f"Election Update: {phase} Phase Announced",
                "body_html": f"<p>The <strong>{phase}</strong> phase of elections is scheduled for <strong>{date}</strong>.</p>",
            },
            queue="notifications.email",
        )
        send_inapp.apply_async(
            kwargs={
                "user_id": user_id,
                "title": f"Election: {phase}",
                "body": f"{phase} scheduled for {date}.",
                "category": "election",
            },
            queue="notifications.inapp",
        )
