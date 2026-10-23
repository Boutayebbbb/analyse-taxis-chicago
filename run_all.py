"""
run_all.py — exécute le pipeline complet (prétraitement, analyses, figures).

Prérequis : les 11 fichiers annuels dans DATA/data_separee_2013-2023/
(voir PRE/01_download.py et le README).

Usage : python run_all.py
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    'PRE/02_fusion.py',
    'PRE/03_preprocess.py',
    'PY/01_distributions/distributions.py',
    'PY/02_evolution_annuelle/evolution_annuelle.py',
    'PY/03_statistiques_descriptives/statistiques_descriptives.py',
    'PY/04_tests_hypotheses/tests_hypotheses.py',
    'PY/05_regression/regression_Q2.py',
    'PY/05_regression/regression.py',
    'PY/06_plages_horaires/plages_horaires_Q3.py',
    'PY/06_plages_horaires/plages_horaires.py',
    'PY/06_plages_horaires/posthoc_heatmap.py',
]

for step in STEPS:
    print(f"\n{'=' * 70}\n  {step}\n{'=' * 70}", flush=True)
    subprocess.run([sys.executable, os.path.join(ROOT, step)], check=True)
print("\nPipeline terminé : résultats dans RESULTS/, figures dans FIG/")
