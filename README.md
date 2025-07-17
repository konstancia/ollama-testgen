
# 🧪 Ollama TestGen — AI-Generated QA Dashboard

This project helps QA teams **automatically generate manual and automation test cases** from Jira requirements using AI models (via Ollama), and visualize/manage them through a beautiful **React + FastAPI dashboard**.

---

## 🚀 Features

- ✅ Pulls tickets from Jira using Jira API + custom label filtering
- 🧠 Generates test cases using local LLMs (via Ollama)
- 📝 Manual and Automation test generation
- 📎 Attaches test files and comments back to Jira
- 🌐 Dashboard UI to preview and manage generated test cases
- 🔄 Regenerate button per ticket
- 🔍 Filter & Search by status or keyword

---

## 📁 Folder Structure

<img width="625" height="311" alt="Screenshot 2025-07-17 at 3 35 13 PM" src="https://github.com/user-attachments/assets/4384a9eb-e405-49bb-9e9a-a6ea0ec9e29c" />


---

## ⚙️ Prerequisites

- Python 3.9+
- Node.js + npm
- Ollama installed locally (`mistral` model)
- Jira token
- Git

---

## 🧪 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/konstancia/ollama-testgen.git
cd ollama_testgen

JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_DOMAIN=yourcompany.atlassian.net
JIRA_PROJECT=QA

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8002

cd frontend
npm install
npm start

The dashboard will open at:
👉 http://localhost:3000

🛠️ Usage
Tickets with the label (e.g. Hackathon) will be fetched.

Generated test cases are saved and attached to Jira.
Use the dashboard to search, preview, and regenerate test cases.
Click 📄 Manual or 📄 Auto to preview test content.
Click Regenerate to refresh test cases.

🤝 **Collaborating**
To collaborate with your team:

Push this project to GitHub
Invite teammates under Settings → Collaborators
Share this repo and setup instructions

📌 Notes
Models are run via Ollama

React UI styled with Tailwind + shadcn/ui (optional)
Jira API uses basic auth with API token
Modify JQL in main.py to match your workflow

📣 Credits
Created by: @konstancia
Built with: 🧠 Ollama · ⚡ FastAPI · ⚛️ React

