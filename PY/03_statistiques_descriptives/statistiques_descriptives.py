"""
PY/03_statistiques_descriptives/statistiques_descriptives.py
------------------------------------------------------------
Statistiques descriptives de P, D et L pour la référence (2013-2020)
et le test (2021).
Sortie : RESULTS/stats_descriptives.csv
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
TRAIN = pd.read_csv(os.path.join(BASE, 'DATA', 'chicago_taxi_train.csv'))
TEST = pd.read_csv(os.path.join(BASE, 'DATA', 'chicago_taxi_test.csv'))
OUT = os.path.join(BASE, 'RESULTS', 'stats_descriptives.csv')

VARS = {'P (trip_total, $)': 'trip_total',
        'D (trip_seconds, s)': 'trip_seconds',
        'L (trip_miles)': 'trip_miles'}

rows = []
for label, col in VARS.items():
    for name, df in [('Référence 2013-2020', TRAIN), ('Test 2021', TEST)]:
        s = df[col]
        rows.append({'Variable': label, 'Periode': name, 'n': len(s),
                     'Moyenne': round(s.mean(), 4), 'Variance': round(s.var(), 4),
                     'Ecart-type': round(s.std(), 4), 'Mediane': round(s.median(), 4),
                     'Min': round(s.min(), 2), 'Max': round(s.max(), 2)})

res = pd.DataFrame(rows)
res.to_csv(OUT, index=False)
print(res.to_string(index=False))
print(f"\nSauvegarde : {OUT}")
