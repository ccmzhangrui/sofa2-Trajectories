#!/bin/bash
echo "Generating sample data..."
python scripts/generate_sample_data.py --output data/sample_data.csv

echo "Calculating SOFA-2 scores..."
python - <<'PY'
import pandas as pd
from src.sofa2_scoring import calculate_sofa2
df = pd.read_csv('data/sample_data.csv')
df['sofa2'] = df.apply(calculate_sofa2, axis=1)
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
df_scores = pd.read_csv('data/sofa2_scores.csv')
df_labels = pd.read_csv('data/trajectory_labels.csv')
merged = df_scores.groupby('patient_id').mean().merge(df_labels, on='patient_id')
X = merged.drop(columns=['patient_id', 'trajectory'])
y = (merged['trajectory'] != 0).astype(int) # 0 = favorable, others = unfavorable
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
models = train_models(X_train, y_train)
auc = evaluate_models(models, X_val, y_val)
print(f"Validation AUC: {auc:.3f}")
PY
echo "Pipeline complete."
