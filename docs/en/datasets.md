# Datasets, provenance and leakage audit

## Source registry
| Source | Primary purpose | Kaggle folder | Source URL/license status |
|---|---|---|---|
| Cardboard v5 | In-domain detection/counting | `cardboard_v5/` | Original dataset project page, export version and license **not independently verified** from repository records; verify before redistribution. |
| Logistics v10 | Separate-domain test and optional future mixed training | `logistics_v10/` | Original dataset project page, export version and license **not independently verified** from repository records; verify before redistribution. |

Mounted combined archive path: `/kaggle/input/datasets/wafabila/boxcount-vision-dataset`. Dataset nickname/version ('v5', 'v10') is **not** enough to identify a canonical upstream URL. Add exact original URLs, author, release, attribution, license, access date and any dataset-specific restrictions only after verifying them.

## Inventory (after known local clean-up)
| Dataset | Split | Images | Positive images | Boxes | Negative images |
|---|---|---:|---:|---:|---:|
| Cardboard v5 | train | 8,403 | 8,403 | 143,331 | 0 |
| Cardboard v5 | valid | 539 | 539 | 9,274 | 0 |
| Cardboard v5 | test | 274 | 274 | 2,644 | 0 |
| Logistics v10 | train | 69,616 | 3,128 | 34,529 | 66,488 |
| Logistics v10 | valid | 19,831 | 867 | 9,946 | 18,964 |
| Logistics v10 | test | 9,936 | 449 | 5,060 | 9,487 |

Total images = 108,599. These are **image-label pairs**, not 108,599 independent recording sessions. Do not assume every Logistics negative file contains truly no box; it may represent an unannotated object.

## Audit evidence and interpretation
- `reports/audit/dataset_audit_clean.json`: local exact deduplication metadata; user reported removal of 111 cross-split duplicates before final packaging. Verify this number against the JSON rather than using it for a new publication without inspection.
- `reports/audit/dataset_inventory.csv`: source-separated counts shown above.
- `reports/audit/invalid_annotation_audit.csv`: no invalid annotation pairs were reported by notebook structural checks.
- `reports/audit/sha_leakage_audit.json`: zero exact cross-split SHA hash groups on mounted input.
- `reports/audit/near_duplicate_candidates_sample.csv`: sampled dHash screening (0 flagged in sampled run), **not exhaustive near-duplicate certification**.
- `reports/audit/filename_audit.json`: records an intermediate filename-rewrite status (`PASS_FILENAME_REWRITE_PENDING_CRC`); final ZIP CRC validation was a separate packaging check, not the contents of this intermediate file.

## Further checks needed
Group frames by original source video, camera and scene; inspect near-identical transformed images across partitions; review duplicate bounding boxes and multi-box occlusions; stratify performance by count and positive/negative scenes; log annotation provenance and licensing. If dataset license prohibits redistribution, keep data off public GitHub and provide instructions to fetch from original provider.
