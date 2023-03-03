from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
import os
from typing import Optional

from urllib3.exceptions import HTTPError
import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

GITLAB_URL = os.getenv('GITLAB_URL')
TOKEN = os.getenv('GITLAB_TOKEN')

if not TOKEN or not GITLAB_URL:
    logger.error("No gitlab URL or Token")
    raise RuntimeError("No gitlab URL or Token")

UserID = int


@dataclass
class ClosedIssue:
    name: str
    url: str
    short_ref: str
    champion: str
    milestone: Optional[str]


@dataclass
class OpenedIssue:
    name: str
    url: str
    short_ref: str
    milestone: Optional[str]


def get_closed_issues() -> dict[str, list[ClosedIssue]]:
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    period_start = datetime(yesterday.year, yesterday.month, yesterday.day, hour=15, minute=00)
    period_end = datetime(today.year, today.month, today.day, hour=15, minute=00)
    try:
        result = httpx.get(
            f'{GITLAB_URL}/api/v4/issues?private_token={TOKEN}&scope=all&state=closed&updated_after={period_start.isoformat()}&updated_before={period_end.isoformat()}'
        )
    except HTTPError as err:
        logger.error(f'Error during fetch: {err}')
        raise

    issues = result.json()
    heroes: dict[str, list[ClosedIssue]] = defaultdict(list)
    for issue in issues:
        if not issue:
            continue

        closed_at = datetime.fromisoformat(issue['closed_at'].replace('Z', ''))
        print(issue['title'], closed_at, period_start)
        if closed_at < period_start:
            continue

        champion: str = (issue.get('assignee', {}) or {}).get('name', 'Unknown hero')

        heroes[champion].append(
            ClosedIssue(
                name=issue['title'],
                url=issue['web_url'],
                short_ref=issue['references']['full'],
                champion=champion,
                milestone=(issue.get('milestone', {}) or {}).get('title')
        ))

    return heroes




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
            short_ref=issue['references']['full'],
            milestone=(issue.get('milestone', {}) or {}).get('title'))
        for issue in issues if issue
    ]

    return parsed


