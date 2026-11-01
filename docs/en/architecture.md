# System architecture and API

## Runtime overview
`frontend/` React + TypeScript + Vite → HTTP `backend/` FastAPI → trusted local YOLO `models/champion/boxcount_champion.pt` → class-0 detections → count and box preview. Separately, `reports/` is read-only historical experiment evidence.

## API contract
| Method | Endpoint | What it means |
|---|---|---|
| GET | `/api/v1/health` | API running, model file presence; **not a forward-pass test** |
| GET | `/api/v1/experiments` | Saved Kaggle `research_report.json` and CSV summaries |
| GET | `/api/v1/history` | RAM-only recent inference metadata (cleared on restart) |
| POST | `/api/v1/analyze/image` | Multipart `file` JPEG/PNG/WebP/BMP; per-image count and boxes |
| POST | `/api/v1/analyze/video` | Multipart `file` MP4/AVI/MOV/MKV/WebM; sampled per-frame counts |
| GET | `/api/v1/files/{filename}` | Generated annotated preview JPEG |

Settings in `backend/.env.example` include model location, `BOXCOUNT_MAX_UPLOAD_MB` (default 100), `BOXCOUNT_MAX_VIDEO_SECONDS` (default 120), `BOXCOUNT_VIDEO_SAMPLE_FPS` (default 3), `BOXCOUNT_MAX_VIDEO_FRAMES` (default 360), `BOXCOUNT_CONFIDENCE` (default .25), `BOXCOUNT_IOU` (default .5), image size, device and CORS origins. Do not equate a `count` field over separate video frames with packages uniquely crossing the camera.

## Image workflow
Validate upload extension/size → safely decode pixels → YOLO predict class 0 → rectangles and confidence → one count for current image → saved preview link → in-memory history.

## Video workflow
Validate duration/FPS/frame budgets → sample frames → YOLO predict each selected frame → return per-frame count timeline. **No persistent track ID, association of same physical box across frames, or crossing-line count.**

## Production caveats
No login or long-term storage. Validate uploaded file content, not only extension. Inference involves nontrivial CPU/GPU work, local outputs and model-loading risks. Keep endpoint private until ingress, auth, quotas, scanning, monitoring and retention controls are implemented.
