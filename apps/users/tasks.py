import random
from celery import shared_task
from apps.utils.utils import send_code


@shared_task(name="send_to_email")
def send_email(code,email):
    task = send_code(code,email)
    
    if task:
        return f"Coden sent to user {email}"
    
    return "Error sending"