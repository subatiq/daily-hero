import os
import smtplib
from dotenv import load_dotenv
import markdown

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

load_dotenv()

MESSAGE_SUBJECT = os.getenv('MESSAGE_SUBJECT', 'Итоги дня')
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', -1))


def send_email(target_email: str, body: str):
    addr_from = EMAIL
    password  = EMAIL_PASSWORD
    if addr_from is None or password is None:
        logger.error('EMAIL of EMAIL_PASSWORD are not specified')
        return

    if not SMTP_SERVER or SMTP_PORT == -1:
        logger.error('SMTP server is not configured')
        return

    msg = MIMEMultipart()
    msg['From']    = addr_from
    msg['To']      = target_email
    msg['Subject'] = MESSAGE_SUBJECT

    head = '''
    <meta charset=utf-8>
    <style>
        body {
            font-size: 16px;
        }
    </style>
    '''

    html = f'<html><head>{head}</head><body>{markdown.markdown(body)}</body></html>'
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(addr_from, password)
    logger.info('Logged in to SMTP')
    server.sendmail(addr_from, target_email, msg.as_string())

    logger.info(f'Sent email to {target_email}')

