# BoxCount Vision Backend — FastAPI

The API wraps trusted local YOLO weights and exposes **real** image inference, sampled-frame video counting, and **read-only** Kaggle reports. See [root README](../README.md), [architecture](../docs/en/architecture.md), [deployment](../docs/en/deployment.md), and [testing](../docs/en/testing.md).

## Local setup

```powershell
cd "D:\porto\100 day\day 28\BoxCount Vision\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest -q
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Model: `../models/champion/boxcount_champion.pt` is local and Git-ignored. Trusted source only. Open `http://127.0.0.1:8000/docs`.

| Endpoint | Output |
|---|---|
| `GET /api/v1/health` | Running/presence status, not model inference |
| `GET /api/v1/experiments` | Saved Kaggle metrics |
| `GET /api/v1/history` | Recent RAM-only results |
| `POST /api/v1/analyze/image` | Detection boxes and per-image count |
| `POST /api/v1/analyze/video` | Sampling timeline, **not** tracking |
| `GET /api/v1/files/{filename}` | Preview JPEG |

Defaults: 100 MB upload, max 120 sec video, 3 sample FPS, 360 frames, `conf=.25`, `iou=.5`, `imgsz=640`, local CPU. Inspect `.env.example` and adjust to hardware; performance outside controlled test environment is unmeasured. External deployment requires user authentication, TLS, rate limits, media scanning, CORS restriction and cleanup.
