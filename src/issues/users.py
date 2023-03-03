import os
import httpx
from dotenv import load_dotenv
from loguru import logger
from urllib3.exceptions import HTTPError

load_dotenv()

TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_URL = os.getenv('GITLAB_URL')

BLACKLIST = os.getenv('BLACKLIST', '').split('|')


def get_user_emails() -> list[str]:
    try:
        result = httpx.get(
            f'{GITLAB_URL}/api/v4/users?exclude_external=true&without_project_bots=true&private_token={TOKEN}'
        )
    except HTTPError as err:
        logger.error(f'Error during fetch: {err}')
        raise

    users = result.json()

    logger.info(f"Got users: {users}")

    return [
        user['email'] for user in users if
        user.get('email')
        and user['state'] != 'blocked'
        and 'bot' not in user['username']
        and user.get('email') not in BLACKLIST
        and 'hero' not in (user.get('pronouns') or '')]

