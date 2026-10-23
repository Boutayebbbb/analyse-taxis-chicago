"""
PY/05_regression/regression.py
------------------------------
Nuages de points (échantillon de 3 000 courses) et droites de régression
P ~ L et P ~ D estimées sur l'ensemble des courses nettoyées.
Sortie : FIG/fig03_regression.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
OUT = os.path.join(BASE, 'FIG', 'fig03_regression.png')

df = pd.read_csv(CLEAN, usecols=['trip_total', 'trip_seconds', 'trip_miles'])
samp = df.sample(3000, random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle("Régressions linéaires — Prix vs Distance et Durée\n"
             f"(nuage : échantillon de 3 000 courses ; droites estimées sur {len(df):,} courses)"
             .replace(',', ' '), fontsize=12, fontweight='bold')

for ax, col, xlab in [(axes[0], 'trip_miles', 'Distance L (miles)'),
                      (axes[1], 'trip_seconds', 'Durée D (secondes)')]:
    reg = stats.linregress(df[col].values, df['trip_total'].values)
    x = samp[col].values
    xr = np.linspace(x.min(), x.max(), 200)
    ax.scatter(x, samp['trip_total'].values, alpha=0.15, s=10, color='steelblue')
    ax.plot(xr, reg.intercept + reg.slope * xr, 'r-', lw=2,
            label=f'P = {reg.intercept:.2f} + {reg.slope:.4f}·x\nR² = {reg.rvalue**2:.4f}')
    ax.set_xlabel(xlab)
    ax.set_ylabel('Prix total P ($)')
    ax.set_title(f'P ~ {xlab.split(" ")[0]}')
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(OUT, dpi=130, bbox_inches='tight')
plt.close()
print(f"Sauvegarde : {OUT}")
