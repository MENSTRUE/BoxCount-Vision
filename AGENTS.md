# AGENTS.md — BoxCount Vision

## Role and authority

You are working on **Day 28 / 100 Days of Projects — BoxCount Vision**, a **single-class cardboard-box detection and per-image counting research prototype**. Use the existing repository and saved Kaggle reports as the source of truth. Do not rewrite research history, change split semantics, invent metrics, fabricate demo outputs, or silently broaden product claims. Follow the root README and scientific documentation; when statements conflict, **actual executed artifact and source code win**, and the discrepancy must be documented.

## Hard rules

1. **Evidence-first:** Only report values from executed notebooks and committed `reports/{audit,evaluation,experiments}`. Do not label any synthetic placeholder as empirical results.
2. **Task semantics:** Image count equals number of accepted class-0 detections. Video currently yields **sampled per-frame counts**. No unique carton throughput, ByteTrack, line-crossing or inventory guarantee.
3. **Dataset boundaries:** Cardboard v5 and Logistics v10 are separate domains. Do not mix source-specific metrics or invent source licenses/URLs. Keep original source splits and record provenance/versions/access dates when verified.
4. **Leakage:** Structural audit and 0 exact cross-split SHA groups are NOT exhaustive near-duplicate, sequence, source or augmentation audits. Any potential leak must remain disclosed.
5. **Model selection:** Select candidates on validation only; never use held-out test to choose hyperparameters, model, confidence, IoU or preprocessing. In current run **A only**, B configured but not run; don't claim A beat B.
6. **Metric correctness:** Detection precision/recall/mAP are not counting exact-match accuracy. Use test split source-specific metrics. Counting threshold reported at 0.25; no test-set tuning.
7. **Repository contract:** Preserve root `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `.env.example`, and directories `notebooks/`, `models/`, `reports/`, `assets/`, `backend/`, `frontend/`, `docs/`, `scripts/`, `tests/`. **Never introduce a `datasets/` directory** into the standard repository. Preserve exact directory names. `.gitkeep` for empty directories.
8. **Binary hygiene:** Never git-add `.pt`, raw images/videos, datasets, ZIPs, credentials, caches, giant predictions or private files unless user explicitly requests a reviewed redistribution process. `models/champion/boxcount_champion.pt` expected locally, excluded from Git. Do not `git add -f` by default.
9. **Safe model loading:** Only load trusted, locally trained Kaggle `.pt`; no uploaded weights or remote arbitrary pickle. Treat file input as untrusted; validate extension, size, decoded content, duration, frame budgets.
10. **Security:** Local dev is not production. Protect uploads, avoid exposing secrets or private paths, implement retention and access controls before remote hosting.
11. **Changes and testing:** Make minimal cohesive changes; run relevant backend `python -m pytest -q`, frontend `npm run build`, and smoke endpoints. Document actual test results; never say 'PASS' without executing.
12. **Documentation:** Keep English root README and Indonesian `docs/id/README.md` aligned. Use real relative paths to existing visual evidence; never reference screenshots not yet committed. Document Before–Now–Next, metrics, source provenance, failure cases, troubleshooting, risk and roadmap.
13. **No accidental overwrites:** Keep Kaggle original notebook, reports and user-provided annotations intact; write new derived outputs to appropriate evidence folders; ask before destructive dataset transformations.
14. **Model training:** Do not train automatically in frontend/backend; experimental retraining belongs in notebooks with reproducible configs and immutable reports.
15. **Deployment claims:** 'Research prototype' only unless independent real-device, latency, security and external-site studies exist.

## Verified metric contract

| Test domain | mAP@50:95 | Count MAE | Exact-count accuracy |
|---|---:|---:|---:|
| Cardboard v5 | 0.73037255 | 2.12408759 | 0.43795620 |
| Logistics v10 | 0.59091206 | 2.41002415 | 0.14683977 |

Validation A mAP@50:95 **0.76114659**; only trained candidate in this export. Source: `reports/experiments/research_report.json` and evaluation CSVs. Do not hardcode these numbers inside application UI; backend reports should be read dynamically.

## Agent work protocol

1. Inspect source and saved artifacts first; specify scope and risk.
2. Keep dataset provenance separate from code dependencies and user-supplied demo assets.
3. Implement and test one component at a time; report commands and outputs.
4. Explain what is genuinely complete vs pending; maintain limitations and do not erase known problems.
5. Commit with conventional commits (`docs:`, `feat:`, `fix:`, `test:`); avoid pushing large artifacts or generated private media.
6. Before merging, confirm no data leakage, fabricated metrics or invalid links were added.

## Module-specific notes

- **Notebook:** preserve original Kaggle dataset mount; 15-epoch Experiment A; never evaluate test during model selection. Experiment B optional and currently unexecuted.
- **Backend:** FastAPI; trusted YOLO weights; report data from CSV/JSON only; `GET /api/v1/health` must not promise successful forward pass; preserve timeout/upload limits.
- **Frontend:** React/TS/Vite; no hardcoded metrics; label chart outputs **per frame**; API failures surfaced clearly; accessible keyboard/contrast and responsive design.
- **Reports:** historical immutable evidence unless a genuinely new reproducible experiment is completed. Create versioned reports rather than replacing past evidence.
- **Assets:** example galleries/scatter plots from real experiment only; externally sourced promotional/demo photos must not be represented as held-out ground truth.

## Definition of done for any task

Code succeeds in relevant automated checks, required artifacts are present and source-linked, sample inference is demonstrated when claiming integration, any persistent risks are documented, and README/AGENTS/translated docs are updated only where justified. A feature not verified on the target hardware is 'implemented, pending validation,' not 'finished and tested.'
