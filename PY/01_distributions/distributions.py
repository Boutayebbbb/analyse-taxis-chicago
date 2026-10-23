"""
PY/01_distributions/distributions.py
------------------------------------
Histogrammes et boxplots de P (trip_total), D (trip_seconds) et L (trip_miles)
sur l'ensemble des courses nettoyées.
Sortie : FIG/fig01_distributions.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
OUT = os.path.join(BASE, 'FIG', 'fig01_distributions.png')

df = pd.read_csv(CLEAN, usecols=['trip_total', 'trip_seconds', 'trip_miles'])

VARS = {
    'trip_total': 'Prix total P ($)',
    'trip_seconds': 'Durée D (secondes)',
    'trip_miles': 'Distance L (miles)',
}

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.suptitle("Distribution des variables — Chicago Taxi Trips (2013-2023)\n"
             f"n = {len(df):,} courses nettoyées".replace(',', ' '),
             fontsize=14, fontweight='bold')

for i, (col, label) in enumerate(VARS.items()):
    ax_h, ax_b = axes[0, i], axes[1, i]
    data = df[col].values

    ax_h.hist(data, bins=60, color='steelblue', edgecolor='white', alpha=0.85)
    ax_h.axvline(data.mean(), color='crimson', lw=1.8, label=f'Moy = {data.mean():.2f}')
    ax_h.axvline(np.median(data), color='orange', lw=1.8, ls='--',
                 label=f'Méd = {np.median(data):.2f}')
    ax_h.set_title(f'Histogramme — {label}', fontsize=10)
    ax_h.legend(fontsize=8)
    ax_h.set_xlabel(label)
    ax_h.set_ylabel('Fréquence')

    ax_b.boxplot(data, orientation='vertical', patch_artist=True,
                 boxprops=dict(facecolor='lightsteelblue'),
                 medianprops=dict(color='crimson', lw=2))
    ax_b.set_title(f'Boxplot — {label}', fontsize=10)
    ax_b.set_ylabel(label)

plt.tight_layout()
plt.savefig(OUT, dpi=130, bbox_inches='tight')
plt.close()
print(f"Sauvegarde : {OUT}")
