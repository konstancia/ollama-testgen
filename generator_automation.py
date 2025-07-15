import requests
from requests.auth import HTTPBasicAuth
import ollama
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("JIRA_PROJECT")
LABEL = "test-needed"  # Change this to your desired label

def generate_tests(requirement, framework="Java + JUnit"):
    prompt = f"""
You are a QA engineer. Based on the following Jira requirement, generate test cases in {framework}:

\"\"\"{requirement}\"\"\"

Include:
- Valid input
- Invalid input
- Edge cases
- Use Java annotations and assertion statements
Output code only.
"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# ✅ Filter by label using JQL
url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
params = {
    "jql": f"project = QA AND issuetype = Story AND labels = Hackathon AND status != Done",
    "fields": "summary,description"
}

response = requests.get(
    url,
    headers={"Accept": "application/json"},
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN),
    params=params
)

if response.status_code != 200:
    print("❌ Failed to fetch Jira tickets")
    print(response.text)
    exit()

stories = response.json()["issues"]

for i, story in enumerate(stories):
    key = story["key"]
    summary = story["fields"]["summary"]
    description = story["fields"].get("description", {}).get("content", [])
    full_text = summary

    # Optional: Append description
    if description:
        text_parts = []
        for block in description:
            for content in block.get("content", []):
                if content.get("text"):
                    text_parts.append(content["text"])
        full_text += "\n" + "\n".join(text_parts)

    print(f"\n📝 Generating tests for {key}: {summary}")
    test_code = generate_tests(full_text)

    filename = f"{key}_Test.java"
    with open(filename, "w") as f:
        f.write(test_code)
    print(f"✅ Saved: {filename}")
