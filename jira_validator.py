import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("JIRA_PROJECT")
LABEL = "Hackathon"  # You can change this to whatever label you use

# ----------------------------
# Helper: Extract plain text
# ----------------------------
def extract_description_text(description):
    if not description:
        return ""
    text_blocks = []
    for block in description.get("content", []):
        for content in block.get("content", []):
            if "text" in content:
                text_blocks.append(content["text"])
    return "\n".join(text_blocks)

# ----------------------------
# Validation logic
# ----------------------------
def has_user_story(text):
    return text.strip().lower().startswith("as a")

def has_acceptance_criteria(text):
    lines = text.splitlines()
    # Count bullet points (starting with - or *)
    bullets = [line for line in lines if line.strip().startswith("-") or line.strip().startswith("*")]
    bullet_ok = len(bullets) >= 2

    # Check for Gherkin-style phrases
    gherkin_ok = all(word in text.lower() for word in ["given", "when", "then"])

    return bullet_ok or gherkin_ok


# ----------------------------
# Fetch Jira stories
# ----------------------------
def fetch_jira_stories():
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
        return []
    return response.json()["issues"]

# ----------------------------
# Main Validation Loop
# ----------------------------
def main():
    tickets = fetch_jira_stories()
    if not tickets:
        print("No tickets found or error occurred.")
        return

    print("\n🔍 Jira Requirement Validation Results:\n")

    for story in tickets:
        key = story["key"]
        summary = story["fields"]["summary"]
        description_raw = story["fields"].get("description")
        description_text = extract_description_text(description_raw)
        print(f"\n--- {key} Description ---\n{description_text}\n------------------------")

        if not description_text.strip():
            print(f"❌ {key} — Empty description")
            continue

        if not has_user_story(description_text):
            print(f"❌ {key} — Missing or malformed user story")
            continue

        if not has_acceptance_criteria(description_text):
            print(f"❌ {key} — Missing or weak acceptance criteria")
            continue

        print(f"✅ {key} — Passed")

# ----------------------------
# Run the script
# ----------------------------
if __name__ == "__main__":
    main()
