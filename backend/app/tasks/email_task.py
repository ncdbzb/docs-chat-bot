import smtplib
from typing import Callable, Dict, Any
from app.config import settings
from app.logger import logger
from app.tasks.celery_app import celery_app
from app.notifications.email import (
    get_approval_email_template,
    get_accepted_request_email_template,
    get_forgot_email_template,
    get_rejected_request_email_template,
    get_admin_approval_email_template,
    get_time_limit_qa_template,
    get_time_limit_test_template
)

template_map: Dict[str, Callable[..., Any]] = {
    'approval': get_approval_email_template,
    'accept': get_accepted_request_email_template,
    'forgot': get_forgot_email_template,
    'reject': get_rejected_request_email_template,
    'admin_approval': get_admin_approval_email_template,
    'qa_time_limit': get_time_limit_qa_template,
    'test_time_limit': get_time_limit_test_template,
}

@celery_app.task
def send_email(**kwargs):
    destiny = kwargs.pop('destiny', None)
    if destiny is None:
        raise ValueError("Missing 'destiny' argument")

    template_func = template_map.get(destiny)
    if not template_func:
        raise ValueError(f"Unknown email destiny: {destiny}")

    try:
        email = template_func(**kwargs)
    except TypeError as e:
        raise ValueError(f"Invalid arguments for email template '{destiny}': {e}")

    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(email)
    except Exception as e:
        logger.info(f"Failed to send '{destiny}' email: {e}")
        raise

    return f"'{destiny}' email was sent"
