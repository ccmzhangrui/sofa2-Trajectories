#!/bin/bash
echo "Generating sample data..."
python scripts/generate_sample_data.py --output data/sample_data.csv

echo "Calculating SOFA-2 scores..."
python - <<'PY'
import pandas as pd
from src.sofa2_scoring import calculate_sofa2

df = pd.read_csv('data/sample_data.csv')
df['sofa2'] = df.apply(calculate_sofa2, axis=1)

# Convert ventilation_mode to numeric column for easier analysis/modeling
VENT_MODE_MAP = {'none': 0, 'high_flow': 1}
df['ventilation_mode'] = df['ventilation_mode'].replace(VENT_MODE_MAP)

df.to_csv('data/sofa2_scores.csv', index=False)
PY

echo "Trajectory modeling..."
python - <<'PY'
import pandas as pd
from src.trajectory import fit_gbtm

df = pd.read_csv('data/sofa2_scores.csv')
scores = df.pivot(index='patient_id', columns='day', values='sofa2')
labels = fit_gbtm(scores, 3)
pd.DataFrame({'patient_id': scores.index, 'trajectory': labels}).to_csv('data/trajectory_labels.csv', index=False)
PY

echo "Training ML models..."
python - <<'PY'
import pandas as pd
from src.ml_model import train_models, evaluate_models
from sklearn.model_selection import train_test_split

df_scores = pd.read_csv('data/sofa2_scores.csv')
df_labels = pd.read_csv('data/trajectory_labels.csv')

# Select only numeric columns (automatically filter out any text columns)
numeric_scores = df_scores.select_dtypes(include={'number'})

# Keep ID column
numeric_scores['patient_id'] = df_scores['patient_id']

# Calculate mean by patient_id (only for numeric columns)
# merged_scores = numeric_scores.groupby('patient_id', numeric_only=True).mean().reset_index()
merged_scores = numeric_scores.groupby('patient_id').mean(numeric_only=True).reset_index()

# Merge trajectory labels
merged = merged_scores.merge(df_labels, on='patient_id')

# Features and labels
X = merged.drop(columns=['patient_id', 'trajectory'])
y = (merged['trajectory'] != 0).astype(int)  # 0 = favorable, others = unfavorable

# Split training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
models = train_models(X_train, y_train)

# Validate AUC
auc = evaluate_models(models, X_val, y_val)
print(f"Validation AUC: {auc:.3f}")
PY

echo "Pipeline complete."
