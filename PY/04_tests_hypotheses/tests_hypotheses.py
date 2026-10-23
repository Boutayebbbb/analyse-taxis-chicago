"""
PY/04_tests_hypotheses/tests_hypotheses.py
------------------------------------------
Q1 : la moyenne de P, D et L change-t-elle en 2021 par rapport à 2013-2020 ?

Pour chaque variable X in {P, D, L} :
    H0 : mu_2021 = mu_ref     vs     H1 : mu_2021 != mu_ref   (bilatéral, alpha = 5 %)

1. Test t à un échantillon : mu_ref = moyenne 2013-2020, considérée comme la
   valeur de référence ; l'échantillon testé est 2021.
2. Test t de Welch à deux échantillons (2021 vs 2013-2020) : vérification qui
   tient compte du fait que la référence est elle-même un échantillon.
3. Taille d'effet d de Cohen : avec n ~ 95 000, même un écart minime est
   significatif ; d mesure l'importance pratique de l'écart.
4. Analyse complémentaire : 2021 vs 2019 (dernière année avant la pandémie),
   pour séparer l'effet de la tendance de long terme de celui de l'année 2021.

Sorties : RESULTS/resultats_Q1.csv, RESULTS/resultats_Q1_2021_vs_2019.csv
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DATA = os.path.join(BASE, 'DATA')
RESULTS = os.path.join(BASE, 'RESULTS')
COLS = ['trip_total', 'trip_seconds', 'trip_miles', 'year']

ref = pd.read_csv(os.path.join(DATA, 'chicago_taxi_train.csv'), usecols=COLS)
test = pd.read_csv(os.path.join(DATA, 'chicago_taxi_test.csv'), usecols=COLS)
ALPHA = 0.05

VARIABLES = {'P (trip_total, $)': 'trip_total',
             'D (trip_seconds, s)': 'trip_seconds',
             'L (trip_miles)': 'trip_miles'}


def cohen_d(a, b):
    """d de Cohen avec écart-type combiné."""
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return (a.mean() - b.mean()) / sp


rows, rows_19 = [], []
ref19 = ref[ref.year == 2019]
print('=' * 72)
print('  Q1 : test t bilatéral (alpha = 5 %) — 2021 vs 2013-2020')
print('=' * 72)
for label, col in VARIABLES.items():
    x, r = test[col].values, ref[col].values
    mu0 = r.mean()
    t1, p1 = stats.ttest_1samp(x, popmean=mu0)
    tw, pw = stats.ttest_ind(x, r, equal_var=False)
    d = cohen_d(x, r)
    diff = x.mean() - mu0
    rows.append({'Variable': label, 'mu_ref_2013_2020': round(mu0, 4),
                 'moyenne_2021': round(x.mean(), 4), 'ecart_type_2021': round(x.std(ddof=1), 4),
                 'n_ref': len(r), 'n_2021': len(x),
                 't_1ech': round(t1, 2), 'p_1ech': p1,
                 't_welch': round(tw, 2), 'p_welch': pw,
                 'difference': round(diff, 4), 'variation_pct': round(100 * diff / mu0, 2),
                 'd_cohen': round(d, 3),
                 'decision': 'Rejeter H0' if p1 < ALPHA else 'Ne pas rejeter H0'})
    print(f"\n  {label}")
    print(f"    mu_ref = {mu0:.2f}   moyenne 2021 = {x.mean():.2f}   "
          f"écart = {diff:+.2f} ({100 * diff / mu0:+.1f} %)")
    print(f"    t (1 éch.) = {t1:.2f}   p = {p1:.2e}   |   t (Welch) = {tw:.2f}   p = {pw:.2e}")
    print(f"    d de Cohen = {d:.3f}")

    y19 = ref19[col].values
    t19, p19 = stats.ttest_ind(x, y19, equal_var=False)
    d19 = cohen_d(x, y19)
    rows_19.append({'Variable': label, 'moyenne_2019': round(y19.mean(), 4),
                    'moyenne_2021': round(x.mean(), 4), 'n_2019': len(y19), 'n_2021': len(x),
                    'difference': round(x.mean() - y19.mean(), 4),
                    'variation_pct': round(100 * (x.mean() - y19.mean()) / y19.mean(), 2),
                    't_welch': round(t19, 2), 'p_welch': p19, 'd_cohen': round(d19, 3)})

print('\n' + '=' * 72)
print('  Analyse complémentaire : 2021 vs 2019 (Welch)')
print('=' * 72)
for r19 in rows_19:
    print(f"  {r19['Variable']:<22} 2019 = {r19['moyenne_2019']:9.2f}   2021 = {r19['moyenne_2021']:9.2f}"
          f"   ({r19['variation_pct']:+.1f} %)   t = {r19['t_welch']:+.2f}   p = {r19['p_welch']:.2e}"
          f"   d = {r19['d_cohen']:+.3f}")

pd.DataFrame(rows).to_csv(os.path.join(RESULTS, 'resultats_Q1.csv'), index=False)
pd.DataFrame(rows_19).to_csv(os.path.join(RESULTS, 'resultats_Q1_2021_vs_2019.csv'), index=False)
print(f"\nRésultats sauvegardés dans {RESULTS}")
