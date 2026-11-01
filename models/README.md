# Model artifact policy

Preferred path: `models/champion/boxcount_champion.pt` (locally copied trusted Kaggle export, git-ignored). Baseline and champion directories may contain `.gitkeep`, not model binaries in Git. Experiment A is the only trained candidate in the committed research report; do not label an untrained B as a competing champion. Do not deserialize third-party `.pt` files without trust review. See [model inference limitations](../docs/en/architecture.md).
