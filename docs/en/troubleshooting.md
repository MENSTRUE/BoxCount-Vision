# Troubleshooting and FAQ

## Frequent issues
| Symptom | Likely root cause | Check / resolution |
|---|---|---|
| API disconnected | Backend not running or wrong address | Start Uvicorn on 127.0.0.1:8000, examine UI `.env`, verify CORS |
| Model file missing | Git intentionally excludes `.pt` | Copy trusted Kaggle export to `models/champion/boxcount_champion.pt`; check `BOXCOUNT_MODEL_PATH` |
| Model loads but inference fails | Ultralytics/PyTorch compatibility or resource limit | Inspect FastAPI trace, check CPU/GPU, reinstall compatible versions |
| `npm run build` fails | TypeScript/Node dependencies | Run `npm ci`, inspect first TS error, correct rather than disable type checks |
| Image returns 0 | Genuine negative, confidence, model domain mismatch | Inspect input/annotation and threshold; do not optimize on held-out test |
| Video totals look too large | Per-frame counts are repeated across time | Do not sum as unique boxes; tracking feature is not implemented |
| Metrics missing | Report files not copied into repo | Compare `reports/evaluation/` and `reports/experiments/` names |
| Upload rejected | File too large or codec unsupported | Check `.env` size, duration, FPS and frame caps; use compatible MP4 |
| Git ignores model | Intentional `.gitignore` | Keep weights outside public Git, distribute only when permissions reviewed |
| Unexpected Logistics misses | Domain shift, annotation incompleteness | Manual audit negative scenes and calibration on validation data |

## Common questions
**Can I call 90.67% mAP the counting accuracy?** No. Cardboard exact-count accuracy is ~43.80% in saved test evidence.

**Does it include tracking or line crossings?** No. Video is sampled per-frame detection.

**Is the test leakage-free?** Only exact SHA overlaps were ruled out in mounted input; near-duplicate and sequence-level leakage remain unverified.

**Can I publish the dataset under MIT?** MIT covers this project's own software; third-party dataset terms require separate confirmation.

**Should I retrain immediately?** Not required for MVP demo. First quantify error categories and review original labels. Experiment B is optional and was not run in existing report.
