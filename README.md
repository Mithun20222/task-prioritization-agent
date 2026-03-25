# Task Agent

A Gemini-powered task prioritizer with a clean web UI. Enter tasks in plain English and get them classified as **URGENT**, **IMPORTANT**, or **LOW** — with suggested scheduling.

## Project Structure

```
task-agent/
├── backend/
│   ├── main.py           # FastAPI server
│   └── requirements.txt
└── frontend/
    └── index.html        # Single-file UI
```

## Setup

### 1. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set your Gemini API key

**Windows (recommended):**
Set it as a user environment variable so it persists across sessions:
> System Properties → Environment Variables → User Variables → New
> - Variable name: `GEMINI_API_KEY`
> - Variable value: `your_key_here`

**macOS/Linux:**
```bash
export GEMINI_API_KEY=your_key_here
```

> The key is automatically available to any terminal or app you open. No need to set it every session. If running on a new machine, repeat this step.

### 3. Start the backend

```bash
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`.

### 4. Open the frontend

Just open `frontend/index.html` in your browser. No build step needed.

## Usage

- Type your tasks in plain English in the text box
- Click **Run Agent** (or press `Ctrl+Enter`)
- Tasks are extracted, classified, and sorted by priority
- Click **⏻ exit** to close the session

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/process` | Process task input, returns sorted task list |
| GET | `/health` | Health check |
