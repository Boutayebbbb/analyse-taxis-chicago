"""
PY/02_evolution_annuelle/evolution_annuelle.py
----------------------------------------------
Évolution annuelle de P, D et L (2013-2023) : violin plots du prix et courbe
du prix moyen annuel. Le tableau des moyennes annuelles sert à interpréter Q1.
Sorties : FIG/fig02_evolution_annuelle.png, RESULTS/moyennes_annuelles.csv
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
OUT_FIG = os.path.join(BASE, 'FIG', 'fig02_evolution_annuelle.png')
OUT_CSV = os.path.join(BASE, 'RESULTS', 'moyennes_annuelles.csv')

df = pd.read_csv(CLEAN, usecols=['trip_total', 'trip_seconds', 'trip_miles', 'year'])

annual = df.groupby('year').agg(n=('trip_total', 'size'),
                                P_moyen=('trip_total', 'mean'),
                                D_moyen=('trip_seconds', 'mean'),
                                L_moyen=('trip_miles', 'mean')).round(2)
annual.to_csv(OUT_CSV)
print(annual.to_string())

years = list(annual.index)
data = [df.loc[df.year == y, 'trip_total'].values for y in years]
means = annual['P_moyen'].values
ref_mean = df.loc[df.year <= 2020, 'trip_total'].mean()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Évolution annuelle du prix total — Chicago Taxi (2013-2023)",
             fontsize=13, fontweight='bold')

ax = axes[0]
vp = ax.violinplot(data, positions=range(len(years)), showmedians=True)
for body in vp['bodies']:
    body.set_facecolor('steelblue')
    body.set_alpha(0.7)
ax.plot(range(len(years)), means, 'r--o', markersize=5, label='Moyenne')
ax.set_xticks(range(len(years)))
ax.set_xticklabels([str(y) for y in years], rotation=45)
ax.set_xlabel('Année')
ax.set_ylabel('Prix total ($)')
ax.set_title('Distribution par année (violin)')
ax.legend()

ax2 = axes[1]
ax2.plot(years, means, 'b-o', markersize=7, linewidth=2)
ax2.axhline(ref_mean, color='gray', ls='--', lw=1.2,
            label=f'Moyenne 2013-2020 = {ref_mean:.2f} $')
for k, (y, m) in enumerate(zip(years, means)):
    creux = 0 < k < len(means) - 1 and m < means[k - 1] and m < means[k + 1]
    ax2.annotate(f'${m:.1f}', (y, m), textcoords='offset points',
                 xytext=(0, -14 if creux else 8), ha='center', fontsize=8)
ax2.set_xlabel('Année')
ax2.set_ylabel('Prix moyen ($)')
ax2.set_title('Prix moyen annuel')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_FIG, dpi=130, bbox_inches='tight')
plt.close()
print(f"Sauvegarde : {OUT_FIG}")
