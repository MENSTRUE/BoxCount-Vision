# BoxCount Vision — React research frontend

## Run (Windows PowerShell)

```powershell
cd "D:\porto\100 day\day 28\BoxCount Vision\frontend"
Copy-Item .env.example .env
npm install
npm run build
npm run dev
```

Open http://127.0.0.1:5173 with the companion FastAPI backend on port 8000. The UI reads Kaggle metrics from `GET /api/v1/experiments`; it does not hardcode performance values. Upload image to obtain object detections. Upload short video for **sampled per-frame detection counts** only—there is no ByteTrack, persistent object ID, crossing line, nor production-grade inventory guarantee. UI history is session-scoped on backend restart.

### Before / Now / Next

- Before: Kaggle Day 28 YOLO training, primary Cardboard v5 and external Logistics v10 evaluation.
- Now: genuine inference, preview overlays, count charts, saved experiment metric cards, and audit boundaries.
- Next: error analysis on near-duplicate frames, manual annotation review, threshold selection on validation only, optional mixed-domain Experiment B, persistent storage and production security.
