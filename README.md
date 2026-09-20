# Agentic Blog Generator API

An autonomous blog generation and translation service built with **FastAPI**, **LangGraph**, and **Groq Cloud LLMs**. The agent orchestrates dynamic multi-step workflows to craft SEO-optimized titles, write detailed markdown content, and conditionally route output through specialized multilingual translation pipelines.

---

## 📌 Features

* **Stateful Agent Workflow**: Built on LangGraph state machines (`StateGraph`) with sequential and conditional routing.
* **Autonomous Decision-Making**: Dynamically routes blog generation based on whether translation is requested.
* **Fast Inference via Groq**: Integrated with open-weight models (e.g., `openai/gpt-oss-120b`, `llama-3.3-70b-versatile`) for sub-second text generation.
* **Multilingual Translation**: Context-aware localization into target languages like Hindi and French while preserving markdown structure and idioms.
* **Developer-Ready REST API**: Native interactive Swagger UI (`/docs`), automated OpenAPI spec generation, and lightweight request handling.

---

## 🏗️ Architecture & Workflow
            ┌─────────────────┐
              │      START      │
              └────────┬────────┘
                       │
                       ▼
             ┌───────────────────┐
             │  title_creation   │
             └─────────┬─────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │ content_generation  │
            └──────────┬──────────┘
                       │
         ┌─────────────┴─────────────┐
  (topic only)                (with language)
         │                           │
         ▼                           ▼
      ┌─────┐                  ┌───────────┐
      │ END │                  │   route   │
      └─────┘                  └─────┬─────┘
                                     │
                   ┌─────────────────┴─────────────────┐
             (lang == "hindi")                   (lang == "french")
                   │                                   │
                   ▼                                   ▼
         ┌───────────────────┐               ┌───────────────────┐
         │ hindi_translation │               │french_translation │
         └─────────┬─────────┘               └─────────┬─────────┘
                   │                                   │
                   └─────────────────┬─────────────────┘
                                     │
                                     ▼
                                  ┌─────┐
                                  │ END │
                                  └─────┘
---

## 📁 Project Structure

```text
BlogAgentic/
├── app.py                      # FastAPI web server and routing
├── request.json                # Sample payload for CLI testing
├── test_blog.py                # Automated endpoint test client
├── requirements.txt            # Python dependencies
├── .env                        # Secret environment variables (API keys)
├── .gitignore                  # Files and directories ignored by Git
└── src/
    ├── graphs/
    │   └── graph_builder.py    # LangGraph definition, nodes, and edges
    ├── llms/
    │   └── groqllm.py          # Groq LLM initialization and provider config
    ├── nodes/
    │   └── blog_node.py        # Node functions: generation, routing, translation
    └── states/
        └── blogstate.py        # Pydantic schemas and TypedDict state structures

🚀 Getting Started
## Prerequisites
Python 3.10 to 3.12

Active Groq Cloud API Key

1. Clone and set up virtual environment
git clone <your-repository-url>
cd BlogAgentic

# Create and activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# (macOS/Linux)
# python3 -m venv .venv && source .venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Configure Environment Variables
GROQ_API_KEY=gsk_your_groq_api_key_here
LANGCHAIN_API_KEY=lsv2_your_langsmith_key_here
LANGCHAIN_TRACING_V2=true

⚙️ Running the API
Start the FastAPI application with auto-reload:
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
API Base URL: http://127.0.0.1:8000

Interactive Swagger UI: http://127.0.0.1:8000/docs

Alternative Redoc: http://127.0.0.1:8000/redoc

🧪 Testing the API
Method 1: Using curl with a JSON File
Create a request.json file:
{
  "topic": "Agentic AI",
  "language": "french"
}
Run via PowerShell:
curl.exe -X POST "[http://127.0.0.1:8000/blogs](http://127.0.0.1:8000/blogs)" `
     -H "Content-Type: application/json" `
     -d "@request.json"

Run via Linux/macOS Bash:
curl -X POST "[http://127.0.0.1:8000/blogs](http://127.0.0.1:8000/blogs)" \
     -H "Content-Type: application/json" \
     -d @request.json

Method 2: Python TestClient (test_blog.py)

import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

with open("request.json", "r") as f:
    payload = json.load(f)

response = client.post("/blogs", json=payload)
print("Status Code:", response.status_code)
print("Response:", response.json())

Run test:
python test_blog.py

## to run the app.py from curl command
curl -X POST "http://127.0.0.1:8001/blogs" -H "Content-Type: application/json" -d @request.json

📤 Sample API Response
{
  "data": {
    "topic": "Agentic AI",
    "current_language": "french",
    "blog": {
      "title": "IA Agentique : Plongée Profonde dans la Prochaine Génération de Systèmes",
      "content": "## Introduction à l'IA Agentique\n\nL'IA agentique représente un changement fondamental..."
    }
  }
}

☁️ Deployment (Render Free Web Service)
Push your code to a public/private GitHub repository.

Log into Render and select New + → Web Service.

Connect your repository and configure:

Runtime: Python 3

Build Command: pip install --upgrade pip && pip install -r requirements.txt

Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

Instance: Free Tier

Add your Environment Variables (GROQ_API_KEY, etc.) in the dashboard settings.

Click Deploy. Your live endpoint will be accessible at https://<service-name>.onrender.com/docs.

