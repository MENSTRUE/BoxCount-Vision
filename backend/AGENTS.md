# Backend agent rules

- Use only locally trusted Kaggle-exported `boxcount_champion.pt`.
- Never claim that video sampling is tracking or throughput counting.
- The single-class target is YOLO class ID 0 (`box`).
- Saved reports are read-only source of truth, never fabricate accuracy or latency.
- Tests should pass without loading weights; integration test against real artifact on operator machine.
- Keep security restrictions on upload size, extension and artifact previews.
