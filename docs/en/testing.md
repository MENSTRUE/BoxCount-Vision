# Testing and acceptance criteria

## Re-runable checks
- Backend unit/API: `cd backend; python -m pytest -q` (tests at `backend/tests/test_api.py`). Prior development reported 6/6; rerun in user's environment before publishing a new badge.
- Frontend: `cd frontend; npm ci; npm run build; npm run dev`. A build was not independently confirmed when the delivered app was originally constructed.
- API smoke: `GET http://127.0.0.1:8000/api/v1/health` and `/api/v1/experiments` return meaningful fields, not hardcoded metric numbers.
- Image: upload a valid cardboard image; record upload dimensions, count, bounding boxes, confidences, elapsed time, preview; test corrupt image and unsupported extension.
- Video: upload a short MP4, record per-frame timeline, correctly labeled as frame counts; test oversized and unreadable video.
- Research: compare dashboard values to saved source CSV/JSON, never to qualitative sample photos.

## Boundaries
A green health badge means HTTP connectivity, not verified model behavior. Unit tests may use mocked model behavior and therefore do not prove real `.pt` inference. End-to-end model loading must be tested with a trusted artifact, and published findings must distinguish executed and planned work.
