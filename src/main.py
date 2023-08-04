import os
from dotenv import load_dotenv
from loguru import logger
from src.issues.issues import get_closed_issues, get_opened_issues
from src.issues.formating import format_notification
from src.issues.notification import send_email

load_dotenv()

ENV = os.getenv('ENV', 'DEBUG')
DEBUG_EMAIL = os.getenv('DEBUG_EMAIL')
TARGET_EMAIL = os.getenv('TARGET_EMAIL')

if not TARGET_EMAIL:
    raise ValueError("TARGET_EMAIL should be set")

def send_daily_report() -> None:
    closed = get_closed_issues()
    opened = get_opened_issues()
    message = format_notification(closed, opened)

    if message is None:
        logger.info('Nothing to send today')
        return

    email = DEBUG_EMAIL if DEBUG_EMAIL else []

    if not ENV == 'DEBUG':
        email = TARGET_EMAIL

    logger.info(f'Will use email: {email}')

    send_email(email, message)


if __name__ == "__main__":
    send_daily_report()
