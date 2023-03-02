from dataclasses import dataclass
from datetime import datetime, timedelta
import os
import httpx
from dotenv import load_dotenv
from loguru import logger
from urllib3.exceptions import HTTPError

load_dotenv()

TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_URL = os.getenv('GITLAB_URL')

UserID = int


@dataclass
class ClosedIssue:
    name: str
    url: str
    short_ref: str
    champion: str


@dataclass
class OpenedIssue:
    name: str
    url: str
    short_ref: str


def get_closed_issues() -> list[ClosedIssue]:
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    period_start = datetime(yesterday.year, yesterday.month, yesterday.day, hour=15, minute=00).isoformat()
    period_end = datetime(today.year, today.month, today.day, hour=15, minute=00).isoformat()
    try:
        result = httpx.get(
            f'{GITLAB_URL}/api/v4/issues?private_token={TOKEN}&scope=all&state=closed&updated_after={period_start}&updated_before={period_end}'
        )
    except HTTPError as err:
        logger.error(f'Error during fetch: {err}')
        raise

    issues = result.json()
    parsed = [
        ClosedIssue(
            name=issue['title'],
            url=issue['web_url'],
            short_ref=issue['references']['short'],
            champion=(issue.get('assignee', {}) or {}).get('name', 'Unknown'))
        for issue in issues if issue
    ]

    return parsed




def get_opened_issues() -> list[OpenedIssue]:
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    period_start = datetime(yesterday.year, yesterday.month, yesterday.day, hour=15, minute=00).isoformat()
    period_end = datetime(today.year, today.month, today.day, hour=15, minute=00).isoformat()
    try:
        result = httpx.get(
            f'{GITLAB_URL}/api/v4/issues?private_token={TOKEN}&scope=all&state=opened&created_after={period_start}&created_before={period_end}'
        )
    except HTTPError as err:
        logger.error(f'Error during fetch: {err}')
        raise

    issues = result.json()
    parsed = [
        OpenedIssue(
            name=issue['title'],
            url=issue['web_url'],
            short_ref=issue['references']['short'])
        for issue in issues if issue
    ]

    return parsed


