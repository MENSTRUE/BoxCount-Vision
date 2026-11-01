# BoxCount Vision Frontend — React + Vite

Scientific research console for the [BoxCount Vision API](../backend/README.md). **Do not mistake saved Kaggle held-out metrics for fresh uploaded-image accuracy**. The app provides Overview, Image Detection, Video Analysis and Research & Audit. A video reports **sampled frame counts**, not unique objects or warehouse throughput.

## Run

```powershell
cd "D:\porto\100 day\day 28\BoxCount Vision\frontend"
Copy-Item .env.example .env
npm ci
npm run build
npm run dev
```

Visit `http://127.0.0.1:5173`, ensure FastAPI on `127.0.0.1:8000`. Edit frontend `.env` only to match the documented API URL. If the model cannot load, verify the backend logs and `models/champion/boxcount_champion.pt`. The UI should not fabricate values on errors.

## Validity and testing

`npm run build` is the automated TypeScript/Vite build gate. Run browser smoke tests for image previews and count, short MP4 timeline, invalid file, missing model, disconnected API and mobile layout. API health 'connected' does not guarantee a successful model prediction. See [testing](../docs/en/testing.md), [troubleshooting](../docs/en/troubleshooting.md), and [root README](../README.md).
