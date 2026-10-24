# Analyse statistique des courses de taxi à Chicago (2013-2023)

Étude statistique de **975 939 courses de taxi** de Chicago, issues d'un échantillon aléatoire de
1 177 937 trajets (≈ 108 000 par an) du dataset public *Chicago Taxi Trips*.
Trois questions sont traitées sur le prix **P**, la durée **D** et la distance **L** des courses :

1. **Tests d'hypothèse** : la moyenne de P, D et L change-t-elle en 2021 par rapport à 2013-2020 ?
2. **Corrélation et régression** : comment le prix dépend-il de la distance et de la durée ?
3. **ANOVA et post-hoc de Bonferroni** : existe-t-il une plage horaire de pointe, et le prix varie-t-il selon l'heure ?

## Résultats principaux

### Q1 — 2021 vs 2013-2020 (test t, α = 5 %)

| Variable | Moyenne 2013-2020 | Moyenne 2021 | Variation | t | d de Cohen |
| --- | --- | --- | --- | --- | --- |
| Prix P (USD) | 29,04 | 34,51 | +18,8 % | 87,05 | 0,28 |
| Durée D (s) | 1 452,1 | 1 536,3 | +5,8 % | 32,47 | 0,09 |
| Distance L (miles) | 8,34 | 9,54 | +14,4 % | 55,41 | 0,17 |

H0 est rejetée pour les trois variables (confirmé par un test de Welch), mais les tailles d'effet sont faibles.
**Analyse critique :** le prix moyen est passé de 19,79 USD en 2013 à 34,87 USD en 2019. Comparé à 2019, le prix de
2021 est quasiment inchangé (−1,0 %, d = −0,02) : la hausse reflète la **tendance de long terme** et non un
effet propre à 2021. Le seul changement notable en 2021 est une durée plus courte à distance égale (−6,6 %).

### Q2 — Régression linéaire (MCO, 975 939 courses)

| Modèle | Équation | R² |
| --- | --- | --- |
| P ~ L | P = 9,73 + 2,430 · L | 0,714 |
| P ~ D | P = 8,12 + 0,01536 · D | 0,510 |
| **P ~ L + D** | **P = 5,45 + 1,902 · L + 0,005994 · D** | **0,758** |

Corrélations : r(P, L) = 0,845 ; r(P, D) = 0,714. La distance est le facteur dominant (≈ 1,90 USD/mile),
la durée ajoute une tarification à l'attente (≈ 0,36 USD/min).

### Q3 — Plages horaires (ANOVA + Bonferroni)

- ANOVA : F = 1 936,64, p ≈ 0, mais **η² = 0,0098** : l'heure explique moins de 1 % de la variance du prix.
- Plage de pointe en volume : **[16h-20h[** (254 812 courses, 26,1 %).
- Prix moyen maximal : [12h-16h[ (32,95 USD) ; minimal : [00h-04h[ (24,69 USD).
- Post-hoc de Bonferroni (Welch) : **14 paires sur 15** significatives ; [08h-12h[ et [16h-20h[ ont des prix identiques.
- r(P, plage) = 0,032 : relation non monotone, d'où le choix de l'ANOVA.

## Méthodologie

- **Fusion** des 11 fichiers annuels avec conversion du séparateur décimal (virgule → point).
- **Nettoyage** : suppression des valeurs manquantes ou nulles, puis filtres de plausibilité
  (P ≥ 3,25 USD, D ≥ 60 s, L ≥ 0,1 mile, vitesse ≤ 80 mph). Les bornes basses de la méthode IQR étant négatives,
  ces filtres sont nécessaires pour éliminer les erreurs de saisie (prix de 0,01 USD, courses d'une seconde).
- **Outliers** : méthode IQR (k = 3) sur P, D et L.
- **Tests** : t à un échantillon et de Welch, d de Cohen, ANOVA à un facteur avec η², post-hoc de Bonferroni
  (15 tests de Welch, p corrigée × 15), corrélation de Pearson, régressions simple et multiple.

Les limites de l'étude (échantillonnage, année 2013 incomplète, référence hétérogène, prix incluant les
pourboires) sont discutées dans le rapport.

## Structure du projet

```
├── PRE/
│   ├── 01_download.py        Extraction de l'échantillon depuis BigQuery
│   ├── 02_fusion.py          Fusion des 11 fichiers annuels
│   └── 03_preprocess.py      Nettoyage, outliers, variables dérivées, split 2013-2020 / 2021
├── PY/
│   ├── 01_distributions/            Histogrammes et boxplots
│   ├── 02_evolution_annuelle/       Moyennes annuelles
│   ├── 03_statistiques_descriptives/
│   ├── 04_tests_hypotheses/         Q1
│   ├── 05_regression/               Q2
│   └── 06_plages_horaires/          Q3 (ANOVA, post-hoc, figures)
├── DATA/data_separee_2013-2023/     Échantillon annuel (2013.csv … 2023.csv)
├── RESULTS/                         Résultats chiffrés (CSV, JSON)
├── FIG/                             Figures
├── REP/                             Rapport (PDF + source LaTeX) et présentation
└── run_all.py                       Exécute tout le pipeline
```

## Exécution

```bash
pip install -r requirements.txt
python run_all.py
```

Le pipeline recrée les fichiers intermédiaires dans `DATA/`, les résultats dans `RESULTS/` et les figures
dans `FIG/`. L'échantillon annuel est fourni dans le dépôt ; `PRE/01_download.py` permet d'en extraire un
nouveau depuis BigQuery (`bigquery-public-data.chicago_taxi_trips.taxi_trips`).

## Technologies

Python · pandas · NumPy · SciPy · Matplotlib · LaTeX

## Contexte

Projet du module *Data Analytics* (ESISA Fès, 2025-2026), encadré par Pr. Ferdaous Hdioud.
Projet réalisé en groupe de trois étudiants ; j'ai réalisé l'ensemble du développement et des analyses
statistiques.

Source des données : [City of Chicago — Taxi Trips](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew).

**Auteur :** Marouane Boutayeb
