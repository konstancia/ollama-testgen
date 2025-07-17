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

ollama_testgen/
├── backend/ # FastAPI server: fetch Jira, generate tests, serve API
│ ├── main.py
│ ├── generator_manual.py
│ ├── generator_auto.py
│ └── ...
├── frontend/ # React dashboard (port 3000+)
│ ├── src/
│ │ ├── App.jsx
│ │ └── ...
├── manual/test_cases/ # Saved manual test files
├── automation/test_cases/ # Saved automation test files
├── .env # Secret Jira + Ollama API info
└── README.md


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

