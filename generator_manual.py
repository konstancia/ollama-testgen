import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import ollama

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("JIRA_PROJECT")
LABEL = "Hackathon"

# -----------------------------
# Command-line arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--force", action="store_true", help="Force regenerate test cases even if file exists")
args = parser.parse_args()

# -----------------------------
# Helper: Extract plain text from Jira description
# -----------------------------
def extract_description_text(description):
    if not description:
        return ""
    text_blocks = []
    for block in description.get("content", []):
        for content in block.get("content", []):
            if "text" in content:
                text_blocks.append(content["text"])
    return "\n".join(text_blocks)

# -----------------------------
# Generate manual test cases using Ollama
# -----------------------------
def generate_manual_tests(requirement):
    prompt = f"""
You are a manual QA engineer.

Based on the following requirement, generate 3 clear manual test cases in this format:

- **Title**
- **Preconditions**
- **Test Steps**
- **Expected Result**

Requirement:
\"\"\"{requirement}\"\"\"
"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# -----------------------------
# Comment on Jira ticket
# -----------------------------
def add_jira_comment(issue_key, comment_text):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
    )

    if response.status_code == 201:
        print(f"🗨️  Comment added to {issue_key}")
    else:
        print(f"❌ Failed to add comment to {issue_key}: {response.status_code}")
        print(response.text)

# -----------------------------
# Attach file to Jira
# -----------------------------
def attach_file_to_jira(issue_key, file_path):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/attachments"
    headers = {
        "X-Atlassian-Token": "no-check"
    }

    with open(file_path, "rb") as file:
        files = {
            "file": (os.path.basename(file_path), file, "application/octet-stream")
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
        )

    if response.status_code in [200, 201]:
        print(f"📎 Attached file to {issue_key}: {file_path}")
    else:
        print(f"❌ Failed to attach file to {issue_key}: {response.status_code}")
        print(response.text)

# -----------------------------
# Fetch Jira issues using JQL
# -----------------------------
def fetch_jira_stories():
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
    params = {
        "jql": f"project = {PROJECT_KEY} AND issuetype = Story AND labels = {LABEL} AND status != Done",
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
        return []
    return response.json()["issues"]

# -----------------------------
# Main script
# -----------------------------
stories = fetch_jira_stories()
os.makedirs("manual/test_cases", exist_ok=True)

for story in stories:
    key = story["key"]
    summary = story["fields"]["summary"]
    description_raw = story["fields"].get("description")
    description_text = extract_description_text(description_raw)

    full_text = summary
    if description_text:
        full_text += "\n" + description_text

    filename = f"manual/test_cases/{key}_ManualTest.md"
    if os.path.exists(filename) and not args.force:
        print(f"⏭️  Skipping {key} — test case already exists.")
        continue

    print(f"\n📝 Generating manual test cases for {key}: {summary}")
    test_cases = generate_manual_tests(full_text)

    with open(filename, "w") as f:
        f.write(test_cases)
    print(f"✅ Saved: {filename}")

    # Attach + comment
    attach_file_to_jira(key, filename)
    add_jira_comment(key, "✅ Manual test cases generated and attached.")

print("\n🚀 All done!")
