from datetime import datetime
from typing import Optional
from src.issues.issues import ClosedIssue, OpenedIssue


def format_closed_issues(closed_issues: list[ClosedIssue]) -> Optional[str]:
    if not closed_issues:
        return None

    message = f"# 🏆 Герои дня ({datetime.utcnow().date().isoformat()})\n"
    message += "\n## Закрытые сегодня задачки\n"
    for closed in closed_issues:
        message += f'**{closed.champion}**\n\n'
        for issue in [i for i in closed_issues if i.champion == closed.champion]:
            message += f'- ✅ {issue.name} ([{issue.short_ref}]({issue.url}))\n'

        message += '\n'

    return message


def format_opened_issues(opened_issues: list[OpenedIssue]) -> Optional[str]:
    if not opened_issues:
        return None

    message = "\n\n## Открытые сегодня задачки\n"

    for opened in opened_issues:
        message += f'- 🔲 {opened.name} ([{opened.short_ref}]({opened.url}))'

    message += '\n\n(Tecтовая рассылочка)'
    return message


def format_notification(closed_issues: list[ClosedIssue], opened_issues: list[OpenedIssue]) -> Optional[str]:
    closed_message = format_closed_issues(closed_issues) or ""
    opened_message = format_opened_issues(opened_issues) or ""

    message = closed_message + opened_message

    if not message:
        return None

    return message


