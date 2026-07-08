# AI-First CRM — HCP Interaction Module

An intelligent CRM application designed for pharmaceutical representatives to capture and organize interactions with Healthcare Professionals (HCPs) using natural language conversations and AI-driven information extraction.

## Architecture

```
┌─────────────┐     HTTP/REST     ┌──────────────┐     LangGraph     ┌──────────┐
│   React +   │ ◄──────────────► │   FastAPI    │ ◄──────────────► │   Groq   │
│   Redux     │                   │   Backend    │                   │   LLM    │
│   Frontend  │                   │              │                   │ gemma2-9b│
└─────────────┘                   └──────┬───────┘                   └──────────┘
                                         │
                                    ┌────▼─────┐
                                    │PostgreSQL│
                                    │ Database │
                                    └──────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Redux Toolkit, Tailwind CSS v4 |
| Backend | Python, FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| AI Agent | LangGraph, LangChain |
| LLM | Groq API (gemma2-9b-it) |
| Font | Google Inter |

## Features

- **Split-screen UI**: Form (left) + AI Chat (right)
- **AI-controlled form**: All form fields populated via natural language
- **5 LangGraph Tools**:
  1. `log_interaction` — Extract entities and fill the form
  2. `edit_interaction` — Update specific fields
  3. `suggest_followup` — AI-generated next steps
  4. `search_hcp` — Search HCP database
  5. `summarize_interaction` — Professional interaction summary

## Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Groq API key (free at https://console.groq.com)

## Setup Instructions

### 1. Clone the Repository
### Repository

[GitHub Repository](https://github.com/anisha12167/ai-crm-hcp)

### 2. Database Setup
```bash
# Create database (run in psql or pgAdmin)
CREATE DATABASE hcp_crm;
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GROQ_API_KEY and DATABASE_URL

# Seed demo data
python -m app.seed

# Start server
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Open the App
Navigate to [AI CRM Demo](https://ai-crm-hcp-delta.vercel.app)

## LangGraph Agent Architecture

The AI agent uses a ReAct (Reason + Act) loop:

```
User Message → Agent (LLM) → Tool Decision
                                    │
                              ┌─────┴─────┐
                              │   Tools    │
                              │ (execute)  │
                              └─────┬─────┘
                                    │
                              Agent (LLM) → Response
```

1. User sends a natural language message
2. LLM analyzes the message and decides which tool to call
3. Tool executes and returns structured data
4. LLM reads the result and generates a response
5. Form updates are sent to the frontend via Redux

## Demo Prompts

Try these in the AI chat:
```
"Met Dr Sharma regarding CardioX and discussed efficacy results and patient outcomes."
"Update the interaction sentiment to neutral."
"Suggest the next best follow-up action for this doctor."
"Search for cardiologists in the database."
"Generate a summary of this interaction."
```

## Project Structure

```
ai-crm-hcp/
├── frontend/               # React + Redux + Tailwind
│   ├── src/
│   │   ├── app/store.js           # Redux store
│   │   ├── features/              # Redux slices
│   │   ├── components/            # React components
│   │   ├── services/api.js        # Axios API layer
│   │   └── utils/constants.js     # App constants
│   └── ...
├── backend/                # FastAPI + LangGraph
│   ├── app/
│   │   ├── main.py               # FastAPI entry
│   │   ├── agent/                # LangGraph agent
│   │   │   ├── graph.py          # StateGraph construction
│   │   │   ├── tools.py          # 5 AI tools
│   │   │   ├── state.py          # AgentState schema
│   │   │   └── prompts.py        # System prompt
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── routes/               # API routes
│   │   ├── services/             # Business logic
│   │   └── seed.py               # Demo data seeder
│   └── ...
└── README.md
```

## Author


### Anisha Saini


Computer Science Engineering Graduate |  ROUND-1


Built as an AI-powered CRM solution demonstrating conversational AI, information extraction, and full-stack application deployment using modern web technologies.
