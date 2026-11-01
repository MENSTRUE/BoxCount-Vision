# BoxCount Vision — Backend (FastAPI)

Runs trusted, locally exported single-class YOLO detector weights from Kaggle. Research only: uploaded images are not used to train a model. The video endpoint samples frames and counts detected boxes **per frame**; it is **not multi-object tracking**, inventory reconciliation, or exact physical item throughput.

## Setup — Windows PowerShell

```powershell
cd "D:\porto\100 day\day 28\BoxCount Vision\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest -q
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The screenshot of your repo had `boxcount_champion.pt` in `models/baseline/`. Prefer moving it to `models/champion/` (or explicitly set `BOXCOUNT_MODEL_PATH` in backend/.env). If both paths exist, champion wins. No model is included in this delivery. Loading arbitrary `.pt` files is unsafe; only use your own trusted Kaggle export.

Open `http://127.0.0.1:8000/docs`.

## API endpoints

- `GET /api/v1/health` — model presence / connection (does not execute inference)
- `GET /api/v1/experiments` — **saved** Kaggle CSV and research_report.json
- `GET /api/v1/history` — most recent results in server memory (cleared on restart)
- `POST /api/v1/analyze/image` — multipart form-data `file`; JSON count + detections and annotated preview URL
- `POST /api/v1/analyze/video` — multipart form-data `file`; JSON timeline counts (sampled frames, NOT object IDs)
- `GET /api/v1/files/{id}.jpg` — annotated image preview

Inferred counts depend on confidence, IoU, image conditions and label completeness. Video sampling skips frames; it cannot prove how many unique boxes passed a line. 100 MB, 120 seconds, and 360 sampled frames are configured defaults; adjust `.env` to suit your machine. Workloads are serialized through an inference lock and may be slow on CPU. For public deployment add auth, user quotas, cleanup/retention, content scanning, TLS, stricter abuse budgets and persistent storage. Do not publicly expose this research server as-is.
