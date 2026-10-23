"""
PY/06_plages_horaires/posthoc_heatmap.py
----------------------------------------
Visualisation du test post-hoc de Bonferroni : matrice des différences de
prix moyen entre plages (P_i - P_j) annotée par le niveau de significativité,
et prix moyen par plage.
Entrées : RESULTS/resultats_Q3.csv, RESULTS/resultats_Q3_posthoc.csv
Sortie  : FIG/fig05_posthoc_bonferroni.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
RESULTS = os.path.join(BASE, 'RESULTS')
OUT = os.path.join(BASE, 'FIG', 'fig05_posthoc_bonferroni.png')

summary = pd.read_csv(os.path.join(RESULTS, 'resultats_Q3.csv'))
posthoc = pd.read_csv(os.path.join(RESULTS, 'resultats_Q3_posthoc.csv'))
ORDER = list(summary['plage'])
k = len(ORDER)
idx = {s: i for i, s in enumerate(ORDER)}

diff = np.full((k, k), np.nan)
stars = np.full((k, k), '', dtype=object)
for _, r in posthoc.iterrows():
    i, j = idx[r.plage_i], idx[r.plage_j]
    s = '***' if r.p_adj < 0.001 else '**' if r.p_adj < 0.01 else '*' if r.p_adj < 0.05 else 'n.s.'
    diff[i, j], diff[j, i] = r.diff_moyennes, -r.diff_moyennes
    stars[i, j] = stars[j, i] = s

fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [1.15, 1]})
fig.suptitle('Test post-hoc de Bonferroni — Plages horaires vs Prix', fontsize=13, fontweight='bold')

ax = axes[0]
lim = np.nanmax(np.abs(diff))
im = ax.imshow(diff, cmap='RdBu_r', vmin=-lim, vmax=lim)
for i in range(k):
    for j in range(k):
        if i == j:
            ax.text(j, i, '—', ha='center', va='center', color='gray')
        else:
            val = f'{diff[i, j]:+.2f}'.replace('-0.00', '0.00').replace('+0.00', '0.00')
            ax.text(j, i, f'{val}\n{stars[i, j]}', ha='center', va='center', fontsize=8,
                    color='white' if abs(diff[i, j]) > 0.6 * lim else 'black')
ax.set_xticks(range(k))
ax.set_yticks(range(k))
ax.set_xticklabels(ORDER, rotation=30)
ax.set_yticklabels(ORDER)
ax.set_xlabel('Plage j')
ax.set_ylabel('Plage i')
ax.set_title('Différence de prix moyen P̄i − P̄j ($)\n*** p_adj < 0,001   n.s. : non significatif')
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='$')

ax = axes[1]
colors = ['#0D47A1', '#1565C0', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9']
bars = ax.bar(ORDER, summary['moyenne'], color=colors, edgecolor='white')
for b, m in zip(bars, summary['moyenne']):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.3, f'${m:.2f}',
            ha='center', va='bottom', fontsize=8)
ax.set_ylabel('Prix moyen ($)')
ax.set_xlabel('Plage horaire')
ax.set_title('Prix moyen par plage horaire')
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig(OUT, dpi=130, bbox_inches='tight')
plt.close()
print(f"Sauvegarde : {OUT}")
