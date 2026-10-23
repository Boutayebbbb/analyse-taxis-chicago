"""
PY/05_regression/regression_Q2.py
---------------------------------
Q2 : corrélation de Pearson et régressions linéaires (MCO)
     P ~ L   |   P ~ D   |   P ~ L + D
sur l'ensemble des courses nettoyées.
Sortie : RESULTS/resultats_Q2.csv
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
OUT = os.path.join(BASE, 'RESULTS', 'resultats_Q2.csv')

df = pd.read_csv(CLEAN, usecols=['trip_total', 'trip_seconds', 'trip_miles'])
P, L, D = df['trip_total'].values, df['trip_miles'].values, df['trip_seconds'].values
n = len(P)
print(f"n = {n:,} courses")

r_PL, p_PL = stats.pearsonr(P, L)
r_PD, p_PD = stats.pearsonr(P, D)
r_LD, _ = stats.pearsonr(L, D)
print(f"\nr(P, L) = {r_PL:.4f}   r(P, D) = {r_PD:.4f}   r(L, D) = {r_LD:.4f}")

reg_L = stats.linregress(L, P)
reg_D = stats.linregress(D, P)
print(f"\nP ~ L     : P = {reg_L.intercept:.4f} + {reg_L.slope:.4f} L          R2 = {reg_L.rvalue**2:.4f}")
print(f"P ~ D     : P = {reg_D.intercept:.4f} + {reg_D.slope:.6f} D        R2 = {reg_D.rvalue**2:.4f}")

X = np.column_stack([np.ones(n), L, D])
coef, *_ = np.linalg.lstsq(X, P, rcond=None)
resid = P - X @ coef
R2 = 1 - np.sum(resid ** 2) / np.sum((P - P.mean()) ** 2)
rmse = np.sqrt(np.mean(resid ** 2))
print(f"P ~ L + D : P = {coef[0]:.4f} + {coef[1]:.4f} L + {coef[2]:.6f} D   R2 = {R2:.4f}   RMSE = {rmse:.2f} $")

pd.DataFrame([{
    'n_courses': n, 'r_PL': round(r_PL, 4), 'r_PD': round(r_PD, 4), 'r_LD': round(r_LD, 4),
    'reg_PL_b0': round(reg_L.intercept, 4), 'reg_PL_b1': round(reg_L.slope, 4),
    'R2_PL': round(reg_L.rvalue ** 2, 4),
    'reg_PD_b0': round(reg_D.intercept, 4), 'reg_PD_b1': round(reg_D.slope, 6),
    'R2_PD': round(reg_D.rvalue ** 2, 4),
    'reg_multi_b0': round(coef[0], 4), 'reg_multi_bL': round(coef[1], 4),
    'reg_multi_bD': round(coef[2], 6), 'R2_multi': round(R2, 4), 'RMSE_multi': round(rmse, 4),
}]).to_csv(OUT, index=False)
print(f"\nSauvegarde : {OUT}")
