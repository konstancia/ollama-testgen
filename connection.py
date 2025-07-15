import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("JIRA_EMAIL")
token = os.getenv("JIRA_API_TOKEN")
domain = os.getenv("JIRA_DOMAIN")

url = f"https://{domain}/rest/api/3/myself"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, token),
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    print("✅ Successfully connected to Jira!")
else:
    print(f"❌ Failed to connect: {response.status_code}")
    print(response.text)
