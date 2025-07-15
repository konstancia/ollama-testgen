import requests
from requests.auth import HTTPBasicAuth
import ollama
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ticket(BaseModel):
    key: str
    summary: str
    status: str
    manual_test_exists: bool
    automation_test_exists: bool

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002"],  # 👈 Add this!
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock ticket data for testing
@app.get("/api/tickets", response_model=list[Ticket])
def get_tickets():
    return [
        Ticket(
            key="QA-1415",
            summary="Hackathon Test",
            status="To Do",
            manual_test_exists=True,
            automation_test_exists=True
        ),
        Ticket(
            key="QA-1416",
            summary="Battery Indicator",
            status="In Progress",
            manual_test_exists=False,
            automation_test_exists=True
        )
    ]

# Regenerate test case (stub action)
@app.post("/api/tickets/{ticket_key}/regenerate")
def regenerate_test(ticket_key: str):
    print(f"🔁 Regenerating test for {ticket_key}")
    return {"status": "ok", "ticket": ticket_key}



# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("JIRA_PROJECT")
LABEL = "test-needed"  # Change to the label you use in Jira

# -----------------------------
# Extract description text from Jira (ADF format)
# -----------------------------
def extract_description_text(description):
    """
    Converts Atlassian Document Format (ADF) to plain text.
    """
    if not description:
        return ""

    text_blocks = []

    for block in description.get("content", []):
        for content in block.get("content", []):
            if "text" in content:
                text_blocks.append(content["text"])

    return "\n".join(text_blocks)

# -----------------------------
# Generate test code using Ollama
# -----------------------------
def generate_tests(requirement, framework="Java + JUnit"):
    prompt = f"""
You are a QA engineer. Based on the following Jira requirement, generate test cases in {framework}:

\"\"\"{requirement}\"\"\"

Include:
- Valid input
- Invalid input
- Edge cases
- Use Java annotations and assertion statements
Only output the test code.
"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# -----------------------------
# Fetch Jira tickets with a specific label
# -----------------------------
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

# -----------------------------
# Loop through stories and generate tests
# -----------------------------
for i, story in enumerate(stories):
    key = story["key"]
    summary = story["fields"]["summary"]
    description_raw = story["fields"].get("description")
    description_text = extract_description_text(description_raw)

    # Combine summary + description for AI prompt
    full_text = summary
    if description_text:
        full_text += "\n" + description_text

    print(f"\n📝 Generating tests for {key}: {summary}")
    test_code = generate_tests(full_text)

    filename = f"{key}_Test.java"
    with open(filename, "w") as f:
        f.write(test_code)
    print(f"✅ Saved: {filename}")
