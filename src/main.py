import os
from dotenv import load_dotenv
from loguru import logger
from src.issues.issues import get_closed_issues, get_opened_issues
from src.issues.formating import format_notification
from src.issues.notification import send_email
from src.issues.users import get_user_emails

load_dotenv()

ENV = os.getenv('ENV', 'DEBUG')
DEBUG_EMAIL = os.getenv('DEBUG_EMAIL')

def send_daily_report() -> None:
    closed = get_closed_issues()
    opened = get_opened_issues()
    message = format_notification(closed, opened)

    if message is None:
        logger.info('Nothing to send today')
        return

    emails = [DEBUG_EMAIL] if DEBUG_EMAIL else []

    if not ENV == 'DEBUG':
        emails = get_user_emails()

    logger.info(f'Got emails: {emails}')

    send_email(emails, message)


if __name__ == "__main__":
    send_daily_report()
