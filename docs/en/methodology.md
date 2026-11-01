# Research methodology

## Research question
Can an in-domain single-class detector trained on Cardboard v5 detect boxes and count them across source domains? Separate detector accuracy from per-image exact count and external-domain robustness.

## Experimental controls
- Seed: 42. Source train/valid/test splits are preserved, not randomly shuffled.
- Experiment A: YOLOv8n pretrained, 15 epochs, 640 image size, batch 16; 5,000 positive Cardboard training images; 539 validation images.
- Experiment B: mixed Cardboard + Logistics data selection was saved (9,628 train, 1,756 validation), but B **was not trained** (`RUN_EXPERIMENT_B=False`).
- Candidate selection: validation mAP@50:95; only A actually exists, with validation score 0.761146593.
- Final test: original 274 Cardboard images and 9,936 Logistics images; no test sampling for selection.
- Count estimate: count accepted detections at fixed conf=0.25; no ID tracking and no confidence tuning on the test splits.

## Reproduction
Open `notebooks/boxcount-vision.ipynb` on Kaggle. Attach `/kaggle/input/datasets/wafabila/boxcount-vision-dataset`. Confirm `RUN_EXPERIMENT_A`, `RUN_EXPERIMENT_B`, training parameters and package versions; run fresh cells and compare generated `research_report.json`, CSV and plots with committed evidence. The saved full notebook may include outputs and original executable content; do not change code merely to make metrics match. For new experiments use versioned artifacts and a new run ID.

## Quality caveats
Ultralytics reported duplicate object annotations removed on some sample images. Structural bbox checks do not assess semantic completeness or correctness; inspect dense overlaps, backgrounds, frames and source-level duplicates before making stronger generalization claims. Preserve source attribution and licenses.
