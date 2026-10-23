"""
PY/06_plages_horaires/plages_horaires_Q3.py
-------------------------------------------
Q3 : plage horaire de pointe et lien entre le prix P et la plage horaire.

La journée est découpée en 6 plages de 4 heures :
    [00h-04h[, [04h-08h[, [08h-12h[, [12h-16h[, [16h-20h[, [20h-24h[

1. ANOVA à un facteur : H0 : mu_1 = ... = mu_6. Taille d'effet : eta².
2. Test post-hoc de Bonferroni : test t de Welch pour chacune des 15 paires,
   p-valeur corrigée p_adj = min(15 * p, 1), seuil 0,05.
3. Corrélation de Pearson r(P, numéro de plage) : tendance linéaire monotone.

Sorties : RESULTS/resultats_Q3.csv, RESULTS/resultats_Q3_posthoc.csv
"""

import os
import json
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CLEAN = os.path.join(BASE, 'DATA', 'chicago_taxi_clean.csv')
RESULTS = os.path.join(BASE, 'RESULTS')

ORDER = ['[00h-04h[', '[04h-08h[', '[08h-12h[', '[12h-16h[', '[16h-20h[', '[20h-24h[']

df = pd.read_csv(CLEAN, usecols=['trip_total', 'time_slot', 'time_slot_label'])
print(f"n = {len(df):,} courses")

groups = [df.loc[df.time_slot_label == s, 'trip_total'].values for s in ORDER]
counts = np.array([len(g) for g in groups])
means = np.array([g.mean() for g in groups])
stds = np.array([g.std(ddof=1) for g in groups])

print("\nPlage         n         part     moyenne   écart-type")
for s, n, m, sd in zip(ORDER, counts, means, stds):
    print(f"{s}  {n:8,}   {100 * n / counts.sum():5.1f} %   {m:8.2f}   {sd:8.2f}")

# 1. ANOVA + eta²
F, p_anova = stats.f_oneway(*groups)
grand = df['trip_total'].mean()
ss_between = np.sum(counts * (means - grand) ** 2)
ss_total = np.sum((df['trip_total'].values - grand) ** 2)
eta2 = ss_between / ss_total
print(f"\nANOVA : F = {F:.2f}   p = {p_anova:.2e}   eta² = {eta2:.4f}")

# 2. Post-hoc de Bonferroni (Welch)
m = len(ORDER) * (len(ORDER) - 1) // 2
posthoc = []
print(f"\nPost-hoc de Bonferroni ({m} paires, Welch)")
for i in range(len(ORDER)):
    for j in range(i + 1, len(ORDER)):
        t, p = stats.ttest_ind(groups[i], groups[j], equal_var=False)
        p_adj = min(p * m, 1.0)
        posthoc.append({'plage_i': ORDER[i], 'plage_j': ORDER[j],
                        'diff_moyennes': round(means[i] - means[j], 4),
                        't_stat': round(t, 2), 'p_brute': p, 'p_adj': p_adj,
                        'significatif': 'Oui' if p_adj < 0.05 else 'Non'})
        print(f"  {ORDER[i]} vs {ORDER[j]}  diff = {means[i] - means[j]:+6.2f}  "
              f"t = {t:+8.2f}  p_adj = {p_adj:.2e}  {'Oui' if p_adj < 0.05 else 'Non'}")
n_sig = sum(r['significatif'] == 'Oui' for r in posthoc)
print(f"  -> {n_sig}/{m} paires significatives")

# 3. Corrélation P / numéro de plage
r, p_r = stats.pearsonr(df['trip_total'].values, df['time_slot'].astype(float).values)
print(f"\nr(P, plage) = {r:.4f}   p = {p_r:.2e}")

i_vol, i_prix, i_min = int(np.argmax(counts)), int(np.argmax(means)), int(np.argmin(means))
print(f"\nPlage de pointe (volume) : {ORDER[i_vol]} ({counts[i_vol]:,} courses, "
      f"{100 * counts[i_vol] / counts.sum():.1f} %)")
print(f"Prix moyen maximal       : {ORDER[i_prix]} ({means[i_prix]:.2f} $)")
print(f"Prix moyen minimal       : {ORDER[i_min]} ({means[i_min]:.2f} $)")

pd.DataFrame({'plage': ORDER, 'n': counts, 'part_pct': np.round(100 * counts / counts.sum(), 2),
              'moyenne': np.round(means, 4), 'ecart_type': np.round(stds, 4)}
             ).to_csv(os.path.join(RESULTS, 'resultats_Q3.csv'), index=False)
pd.DataFrame(posthoc).to_csv(os.path.join(RESULTS, 'resultats_Q3_posthoc.csv'), index=False)
with open(os.path.join(RESULTS, 'resultats_Q3_tests.json'), 'w', encoding='utf-8') as f:
    json.dump({'n': int(len(df)), 'F': float(F), 'p_anova': float(p_anova), 'eta2': float(eta2),
               'r_P_plage': float(r), 'p_r': float(p_r), 'paires_significatives': n_sig,
               'paires': m}, f, indent=2)
print(f"\nRésultats sauvegardés dans {RESULTS}")
