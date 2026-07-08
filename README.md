# AI-First CRM — HCP Interaction Module

An AI-powered CRM module for pharmaceutical field representatives to log interactions with Healthcare Professionals (HCPs) through a conversational AI assistant.

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
```bash
git clone https://github.com/Dacchu2004/ai-crm-hcp.git
cd ai-crm-hcp
```

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
Navigate to http://localhost:5173

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
"Today I met Dr. Sarah Smith and discussed Product X efficacy. Positive sentiment, shared brochures."
"Change the HCP name to Dr. John Chen and sentiment to negative"
"What follow-up actions should I take?"
"Search for oncologists"
"Summarize this interaction"
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

**Dharshan S** — Round 1 Assignment
