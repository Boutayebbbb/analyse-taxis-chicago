"""
PRE/03_preprocess.py
--------------------
Prétraitement du fichier brut fusionné chicago_taxi_raw.csv.

Pipeline :
  1. Suppression des valeurs manquantes ou nulles (P <= 0, D <= 0, L <= 0)
  2. Filtres de plausibilité (courses physiquement impossibles ou erreurs de saisie) :
       - P >= 3,25 $   (prise en charge minimale d'un taxi à Chicago)
       - D >= 60 s     (course d'au moins une minute)
       - L >= 0,1 mile
       - vitesse moyenne L / D <= 80 mph
  3. Suppression des outliers par la méthode IQR (k = 3) sur P, D et L
  4. Variables dérivées : hour, time_slot (0-5), time_slot_label, trip_minutes
  5. Split temporel : référence 2013-2020 / test 2021

Usage : python PRE/03_preprocess.py
"""

import os
import json
import pandas as pd

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA = os.path.join(BASE, 'DATA')
RAW = os.path.join(DATA, 'chicago_taxi_raw.csv')
CLEAN = os.path.join(DATA, 'chicago_taxi_clean.csv')
TRAIN = os.path.join(DATA, 'chicago_taxi_train.csv')
TEST = os.path.join(DATA, 'chicago_taxi_test.csv')
RESULTS = os.path.join(BASE, 'RESULTS')
os.makedirs(RESULTS, exist_ok=True)

SLOT_LABELS = {
    0: '[00h-04h[', 1: '[04h-08h[', 2: '[08h-12h[',
    3: '[12h-16h[', 4: '[16h-20h[', 5: '[20h-24h['
}
P_MIN, D_MIN, L_MIN, SPEED_MAX = 3.25, 60, 0.1, 80
K_IQR = 3


def iqr_bounds(s, k=K_IQR):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    return q1 - k * (q3 - q1), q3 + k * (q3 - q1)


df = pd.read_csv(RAW, usecols=['trip_total', 'trip_seconds', 'trip_miles',
                               'trip_start_timestamp', 'year'])
steps = {'brut': len(df)}
print(f"Brut                       : {len(df):,} lignes")

# 1. Valeurs manquantes ou nulles
df = df[(df.trip_total > 0) & (df.trip_seconds > 0) & (df.trip_miles > 0)]
steps['invalides'] = steps['brut'] - len(df)
print(f"Valeurs manquantes/nulles  : -{steps['invalides']:,}")

# 2. Filtres de plausibilité
n0 = len(df)
speed = df.trip_miles / (df.trip_seconds / 3600)
df = df[(df.trip_total >= P_MIN) & (df.trip_seconds >= D_MIN)
        & (df.trip_miles >= L_MIN) & (speed <= SPEED_MAX)]
steps['plausibilite'] = n0 - len(df)
print(f"Filtres de plausibilité    : -{steps['plausibilite']:,}")

# 3. Outliers IQR x3 (bornes calculées une fois, puis appliquées ensemble)
n0 = len(df)
bounds = {c: iqr_bounds(df[c]) for c in ['trip_total', 'trip_seconds', 'trip_miles']}
mask = pd.Series(True, index=df.index)
for c, (lo, hi) in bounds.items():
    mask &= df[c].between(lo, hi)
    print(f"  IQR x{K_IQR} {c:<13}: [{lo:.2f} ; {hi:.2f}]")
df = df[mask]
steps['iqr'] = n0 - len(df)
print(f"Outliers IQR x{K_IQR}            : -{steps['iqr']:,}")

# 4. Variables dérivées (horodatages en heure locale de Chicago)
ts = pd.to_datetime(df['trip_start_timestamp'].str.replace(' UTC', '', regex=False),
                    errors='coerce')
df = df.assign(hour=ts.dt.hour)
df = df.dropna(subset=['hour'])
df['hour'] = df['hour'].astype(int)
df['time_slot'] = df['hour'] // 4
df['time_slot_label'] = df['time_slot'].map(SLOT_LABELS)
df['trip_minutes'] = (df['trip_seconds'] / 60).round(2)
df['trip_start_timestamp'] = ts.loc[df.index].dt.strftime('%Y-%m-%d %H:%M:%S')

# 5. Split temporel
train = df[df.year <= 2020].reset_index(drop=True)
test = df[df.year == 2021].reset_index(drop=True)
steps.update(final=len(df), reference=len(train), test=len(test),
             par_annee={int(k): int(v) for k, v in df.year.value_counts().sort_index().items()},
             bornes_iqr={c: [round(lo, 2), round(hi, 2)] for c, (lo, hi) in bounds.items()})

print(f"\nDataset nettoyé            : {len(df):,} courses")
print(f"  Référence (2013-2020)    : {len(train):,}")
print(f"  Test (2021)              : {len(test):,}")
print("\nCourses conservées par année :")
print(df.year.value_counts().sort_index().to_string())

df.to_csv(CLEAN, index=False)
train.to_csv(TRAIN, index=False)
test.to_csv(TEST, index=False)
with open(os.path.join(RESULTS, 'pretraitement.json'), 'w', encoding='utf-8') as f:
    json.dump(steps, f, indent=2, ensure_ascii=False)
print(f"\nFichiers sauvegardés dans {DATA}")
