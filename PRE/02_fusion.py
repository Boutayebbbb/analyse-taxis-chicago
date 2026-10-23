"""
PRE/02_fusion.py
----------------
Fusion des 11 fichiers annuels (2013.csv ... 2023.csv) en un seul fichier
DATA/chicago_taxi_raw.csv, avec ajout d'une colonne `year`.

Les fichiers annuels utilisent la virgule comme séparateur décimal
(ex. "0,01") : les colonnes numériques sont lues comme du texte, la virgule
est remplacée par un point, puis la conversion numérique est appliquée.

Usage : python PRE/02_fusion.py
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'DATA')
SRC = os.path.join(BASE, 'data_separee_2013-2023')
RAW = os.path.join(BASE, 'chicago_taxi_raw.csv')
NUM_COLS = ['trip_total', 'trip_seconds', 'trip_miles']

frames = []
print(f"{'Fichier':<10}{'Lignes':>10}{'Taille (Mo)':>14}")
for year in range(2013, 2024):
    path = os.path.join(SRC, f'{year}.csv')
    df = pd.read_csv(path, dtype={c: str for c in NUM_COLS})
    for col in NUM_COLS:
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['year'] = year
    frames.append(df)
    print(f"{year}.csv{len(df):>10,}{os.path.getsize(path) / 1024**2:>14.2f}")

raw = pd.concat(frames, ignore_index=True)
raw.to_csv(RAW, index=False)
print(f"\nTotal : {len(raw):,} lignes -> {RAW}")
