# AI Chat Skeleton

Minimal FastAPI backend and React (Vite + TypeScript) frontend you can extend into a full AI assistant that understands uploaded files.

## Prerequisites

- Python 3.11+
- Node.js 18+ (for `npm`, `pnpm`, or `yarn`)

## Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Available endpoints:

- `GET /health` &mdash; health check.
- `POST /chat` &mdash; accepts `{ messages: [{ role, content }] }` and echoes the last user message. Swap in your LLM call later.

## Frontend (React + Vite)

```bash
cd frontend
npm install       # or pnpm install / yarn
npm run dev
```

The dev server runs on `http://localhost:5173` and proxies `/api/*` requests to `http://localhost:8000`.

## Next steps

- Plug real model logic into `backend/app/main.py::chat`.
- Add file-upload handling and embedding logic on the backend.
- Expand the React UI with file drop zones, history, and status indicators.

