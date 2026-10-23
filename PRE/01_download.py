"""
PRE/01_download.py
------------------
Extraction d'un échantillon aléatoire du dataset Chicago Taxi Trips
depuis la table publique BigQuery :
    bigquery-public-data.chicago_taxi_trips.taxi_trips

Pour chaque année 2013 -> 2023, environ 108 000 courses sont tirées
aléatoirement (TABLESAMPLE + RAND) et sauvegardées dans un fichier CSV
par année : DATA/data_separee_2013-2023/<année>.csv

Colonnes : trip_total, trip_seconds, trip_miles,
           trip_start_timestamp, trip_end_timestamp

Remarque : dans cette table, les horodatages sont exprimés en heure
locale de Chicago (arrondis au quart d'heure), même s'ils portent
l'étiquette « UTC ».

Prérequis :
    pip install google-cloud-bigquery db-dtypes pandas
    gcloud auth application-default login

Usage :
    python PRE/01_download.py --project VOTRE_PROJET_GCP
"""

import os
import argparse
import pandas as pd

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'DATA')
OUT_DIR = os.path.join(BASE, 'data_separee_2013-2023')
YEARS = range(2013, 2024)
ROWS_PER_YEAR = 108_000

QUERY = """
SELECT trip_total, trip_seconds, trip_miles,
       trip_start_timestamp, trip_end_timestamp
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE EXTRACT(YEAR FROM trip_start_timestamp) = {year}
  AND RAND() < {fraction}
LIMIT {limit}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True, help='Identifiant du projet Google Cloud')
    parser.add_argument('--fraction', type=float, default=0.02,
                        help="Fraction tirée avant la limite (0.02 suffit pour ~108 000 lignes/an)")
    args = parser.parse_args()

    from google.cloud import bigquery
    client = bigquery.Client(project=args.project)
    os.makedirs(OUT_DIR, exist_ok=True)

    for year in YEARS:
        sql = QUERY.format(year=year, fraction=args.fraction, limit=ROWS_PER_YEAR)
        df = client.query(sql).to_dataframe()
        out = os.path.join(OUT_DIR, f'{year}.csv')
        df.to_csv(out, index=False)
        print(f'  {year} : {len(df):,} lignes -> {out}')


if __name__ == '__main__':
    main()
