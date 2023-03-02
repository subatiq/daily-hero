from loguru import logger
from src.issues.issues import get_closed_issues, get_opened_issues
from src.issues.formating import format_notification
from src.issues.notification import send_email
from src.issues.users import get_user_emails


def send_daily_report() -> None:
    closed = get_closed_issues()
    opened = get_opened_issues()
    message = format_notification(closed, opened)

    if message is None:
        logger.info('Nothing to send today')
        return

    emails = get_user_emails()
    logger.info(f'Got emails: {emails}')

    send_email(emails, message)


if __name__ == "__main__":
    send_daily_report()
