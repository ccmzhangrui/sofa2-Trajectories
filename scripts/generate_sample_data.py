import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, default='data/sample_data.csv')
args = parser.parse_args()

rows = []
for pid in range(1, 51):  # 50 synthetic patients
    for day in range(1, 15):  # 14 ICU days
        rows.append({
            'patient_id': pid,
            'day': day,
            'PaO2': np.random.randint(60, 150),
            'FiO2': np.random.choice([0.21, 0.3, 0.5]),
            'ventilation_mode': np.random.choice(['none', 'high_flow']),
            'MAP': np.random.randint(55, 90),
            'vasopressor_dose': np.random.choice([0, 0.05, 0.15]),
            'creatinine': round(np.random.uniform(0.5, 3.5), 2),
            'RRT': np.random.choice([0, 1])
        })
df = pd.DataFrame(rows)
df.to_csv(args.output, index=False)
print(f"Sample data saved to {args.output}")
