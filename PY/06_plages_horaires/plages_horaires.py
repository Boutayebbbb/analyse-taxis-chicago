"""
PY/06_plages_horaires/plages_horaires.py
----------------------------------------
Volume de courses et prix moyen par plage horaire de 4 heures.
Sortie : FIG/fig04_plages_horaires.png
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
OUT = os.path.join(BASE, 'FIG', 'fig04_plages_horaires.png')
ORDER = ['[00h-04h[', '[04h-08h[', '[08h-12h[', '[12h-16h[', '[16h-20h[', '[20h-24h[']
COLORS = ['#1565C0', '#1976D2', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9']

df = pd.read_csv(CLEAN, usecols=['trip_total', 'time_slot_label'])
g = df.groupby('time_slot_label')['trip_total'].agg(['size', 'mean']).reindex(ORDER)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Analyse par plage horaire — Chicago Taxi (2013-2023)\n"
             f"n = {len(df):,} courses".replace(',', ' '), fontsize=12, fontweight='bold')

bars = axes[0].bar(ORDER, g['size'], color=COLORS, edgecolor='white')
axes[0].set_xlabel('Plage horaire')
axes[0].set_ylabel('Nombre de courses')
axes[0].set_title('Volume de courses par plage horaire')
axes[0].tick_params(axis='x', rotation=30)
for b, c in zip(bars, g['size']):
    axes[0].text(b.get_x() + b.get_width() / 2, b.get_height() + 1000,
                 f'{c:,}'.replace(',', ' '), ha='center', va='bottom', fontsize=8)

bars = axes[1].bar(ORDER, g['mean'], color=COLORS, edgecolor='white')
axes[1].set_xlabel('Plage horaire')
axes[1].set_ylabel('Prix moyen ($)')
axes[1].set_title('Prix moyen par plage horaire')
axes[1].tick_params(axis='x', rotation=30)
for b, mval in zip(bars, g['mean']):
    axes[1].text(b.get_x() + b.get_width() / 2, b.get_height() + 0.3,
                 f'${mval:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(OUT, dpi=130, bbox_inches='tight')
plt.close()
print(f"Sauvegarde : {OUT}")
