# HelixDesk AI

**AI-powered customer support platform built with Python, FastAPI, React, and PostgreSQL.**

HelixDesk AI is a full-stack customer support SaaS project designed to help teams manage customer information through a modern web dashboard and authenticated API.

## Features

- 🔐 User registration and login
- 🛡️ JWT-based authentication
- 👥 Customer management API
- 📊 React dashboard interface
- 🐘 PostgreSQL database integration
- 🔄 Database migrations with Alembic
- 🧪 Automated API tests
- ⚡ FastAPI backend and Vite frontend

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Migrations | Alembic |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Project Structure

```text
HelixDesk-AI/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── schemas/
├── frontend/
│   └── src/
├── migrations/
├── tests/
├── .env.example
├── alembic.ini
├── pyproject.toml
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.14 or a compatible Python version
- Node.js and npm
- PostgreSQL

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Debanick41/helixdesk-AI.git
   cd helixdesk-AI
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create your local environment configuration using `.env.example` as a reference. Set your own database connection and other required values in `.env`. Never commit real credentials.

5. Apply database migrations after verifying the migration history:

   ```powershell
   alembic upgrade head
   ```

6. Start the API:

   ```powershell
   uvicorn app.main:app --reload
   ```

   API health check: `http://127.0.0.1:8000/health`

   Interactive API documentation: `http://127.0.0.1:8000/docs`

### Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Use the local URL printed by Vite in your terminal.

## Testing

From the project root, activate the virtual environment and run:

```powershell
pytest
```

## Current Status

HelixDesk AI is under active development. Features and setup instructions may evolve as the project grows.

## Security

- Keep `.env` and all secrets out of version control.
- Use your own PostgreSQL credentials.
- Do not use development settings as production security settings.

## Author

**Debanick Basu**

GitHub: [@Debanick41](https://github.com/Debanick41)
