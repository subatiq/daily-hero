from datetime import datetime
from typing import Optional
from src.issues.issues import ClosedIssue, OpenedIssue, get_closed_issues, get_opened_issues


def format_closed_issues(closed_issues: dict[str, list[ClosedIssue]]) -> Optional[str]:
    if not closed_issues:
        return None

    message = f"# 🏆 Герои дня ({datetime.utcnow().date().isoformat()})\n"
    message += "\n## Закрытые сегодня задачки\n"
    for champion, issues in closed_issues.items():
        message += f'**{champion}**\n\n'
        for issue in issues:
            milestone = f'[{issue.milestone}] ' if issue.milestone else ''
            message += f'- ✅ {milestone}{issue.name} ([{issue.short_ref}]({issue.url}))\n'

        message += '\n'

    return message


def format_opened_issues(opened_issues: list[OpenedIssue]) -> Optional[str]:
    if not opened_issues:
        return None

    message = "\n\n## Открытые сегодня задачки\n"

    for issue in opened_issues:
        milestone = f'[{issue.milestone}] ' if issue.milestone else ''
        message += f'- 🔲 {milestone}{issue.name} ([{issue.short_ref}]({issue.url}))\n'

    message += '\n\n'
    return message


def format_notification(
    closed_issues: dict[str, list[ClosedIssue]],
    opened_issues: list[OpenedIssue]
) -> Optional[str]:
    closed_message = format_closed_issues(closed_issues) or ""
    opened_message = format_opened_issues(opened_issues) or ""

    message = closed_message + opened_message

    if not message:
        return None

    return message

if __name__ == "__main__":
    print(format_notification(get_closed_issues(), get_opened_issues()))
