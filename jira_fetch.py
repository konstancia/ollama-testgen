
from jira import JIRA
import os

jira = JIRA(
    server="https://augusthome.atlassian.net",
    basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

def fetch_stories_by_label(project_key: str, label: str):
    jql = f'project = QA AND issuetype = Story AND status = "To Do" AND labels = "Hackathon"'
    return jira.search_issues(jql, maxResults=5)

