# Local setup and deployment boundaries

## Local Windows workflow
Backend: `cd backend; py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; Copy-Item .env.example .env; python -m pytest -q; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.

Frontend: `cd frontend; Copy-Item .env.example .env; npm ci; npm run build; npm run dev`. Frontend: `http://127.0.0.1:5173`; backend docs: `http://127.0.0.1:8000/docs`.

Weights must be a local **trusted Kaggle** `boxcount_champion.pt` under `models/champion/` or a configured `BOXCOUNT_MODEL_PATH`; `.pt` files are excluded from GitHub. If current model is under `models/baseline/`, backend has a compatibility fallback, but move it to champion for clarity. Keep `.env` private.

## Production readiness (not completed)
Authentication/authorization, HTTPS/TLS, approved CORS, upload rate/size/duration limits and scanning, security assessments, job queues for heavy video tasks, temporary file cleanup and retention, monitoring, backups, versioned model registry, latency and representative deployment-data benchmarks, and rollback plan. No operational deployment or verified CI pipeline should be claimed from a local screenshot.
