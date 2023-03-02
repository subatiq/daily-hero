import os
import smtplib
from dotenv import load_dotenv                                      # Импортируем библиотеку по работе с SMTP
import markdown

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText

from loguru import logger

load_dotenv()

EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def send_email(emails: list[str], body: str):
    addr_from = EMAIL                # Адресат
    password  = EMAIL_PASSWORD                                  # Пароль
    if addr_from is None or password is None:
        logger.error('EMAIL of EMAIL_PASSWORD are not specified')
        return

    msg = MIMEMultipart()                               # Создаем сообщение
    msg['From']    = addr_from                          # Адресат
    msg['To']      = ', '.join(emails)                            # Получатель
    msg['Subject'] = 'Инвиановские герои дня'                   # Тема сообщения
    head = '''
    <meta charset=utf-8>
    <style>
        body {
            font-size: 16px;
        }
    </style>
    '''

    html = f'<html><head>{head}</head><body>{markdown.markdown(body)}</body></html>'
    print(html)
    msg.attach(MIMEText(html, 'html'))                 # Добавляем в сообщение текст

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)           # Создаем объект SMTP
    server.login(addr_from, password)                   # Получаем доступ
    logger.info('Logged in to SMTP')
    server.sendmail(addr_from, emails, msg.as_string())

    emails_str_list = "\n".join(emails)
    logger.info(f'Sent email to {emails_str_list}')

