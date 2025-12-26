# SOFA-2 Trajectories Analysis and Early Prediction

This repository contains the complete code to reproduce the pipeline from:

"Longitudinal SOFA-2 Trajectories, 28-Day Survival, and Machine Learning-Based Early
Prediction in Critically Ill Patients With Sepsis"**

---

Features

- SOFA-2 scoring – complete 6 organ systems, based on latest consensus definitions
- Trajectory modeling – Group-Based Trajectory Modeling (GBTM) via R `traj` package, with
Python fallback (Gaussian Mixture Models)
- Machine learning early prediction – ensemble of LightGBM, XGBoost, and Random Forest
- Explainability – SHAP analysis, feature importance
- Synthetic data generation – clinically plausible trajectories
- End-to-end pipeline – from data preprocessing to model evaluation
--- 

Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sofa2-trajectories-prediction.git
cd sofa2-trajectories-prediction
```
2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Optional: Install R packages if using R-based GBTM
Open an R console:
```R
install.packages("traj")
install.packages("lcmm")
``` 

Project Structure
```
data/
 raw/ - raw data (not included)
 processed/ - processed score and trajectory outputs
 synthetic/ - generated synthetic data
src/
 config.py - global configuration and thresholds
 sofa2_scoring.py - SOFA-2 scoring functions
 trajectory_analysis.py - GBTM modeling
 ml_model.py - machine learning pipeline
scripts/
 generate_realistic_data.py - synthetic data generator
 run_pipeline.sh - end-to-end run script
tests/
 test_sofa2_scoring.py - unit tests
```

Quick Start

Run the complete analysis pipeline **on synthetic data**:
```bash
bash scripts/run_pipeline.sh
```
This will:

1. Generate synthetic data for 1000 patients
2. Calculate SOFA-2 scores
3. Model trajectories (GBTM)
4. Train ML prediction model
5. Produce evaluation plots and metrics in `results/`
--- 

Using Real ICU Data (MIMIC-IV/eICU)

1. Place raw CSV/Parquet files in `data/raw/`
2. Adapt preprocessing in `scripts/generate_realistic_data.py` to load your dataset
 - Ensure data includes: vitals, labs, ventilator mode, vasopressor dose, RRT status, patient
demographics.
3. Run:
```bash
bash scripts/run_pipeline.sh
```
Output
- Plots: ROC curve, calibration plot, feature importance, SHAP summary
- Tables: trajectory group proportions, mortality by group
- Saved model: `models/trajectory_predictor.joblib`


License

MIT License

---

Citation
> If you use this repository, please cite the original publication.


4. How to Run

Generate synthetic data only:

```bash
python scripts/generate_realistic_data.py --n_patients 500 --output_data data/synthetic/
patient_data.csv --output_trajectories data/synthetic/trajectory_labels.csv
```
Run scoring only:
```bash
python src/sofa2_scoring.py
```
Test trajectory modeling independently:
```bash
python src/trajectory_analysis.py
```
**Train model independently**:
```bash
python src/ml_model.py
```

5. Included Code Files
- src/config.py – Contains SOFA‑2 thresholds and global settings
- src/sofa2_scoring.py – Full scoring engine for 6 organ systems
- src/trajectory_analysis.py – Real GBTM + Python fallback
- src/ml_model.py – ML pipeline with training, evaluation, and SHAP
- scripts/generate_realistic_data.py – Synthetic cohort creation
- scripts/run_pipeline.sh – End-to-end execution
- tests/test_sofa2_scoring.py – Unit tests for scoring correctness 