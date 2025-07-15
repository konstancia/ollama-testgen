from jira import JIRA

# Connect to JIRA
jira = JIRA(
    server="https://yourcompany.atlassian.net",
    basic_auth=("your.email@example.com", "your_api_token")
)

# Define your project and label
project_key = "ENG"
label = "ai-test"

# Build your JQL
jql = f'project = {project_key} AND issuetype = Story AND status = "To Do" AND labels = "{label}" ORDER BY created DESC'
print(f"Running JQL: {jql}")

# Fetch issues
issues = jira.search_issues(jql, maxResults=5)

# Display results
for issue in issues:
    print(f"{issue.key}: {issue.fields.summary}")
    print(issue.fields.description)
