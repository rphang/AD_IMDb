# Top 1000 des Films basés sur le score IMDb

Ce projet a pour but de créer une application web permettant d'appliquer de l'analyse de données les 1000 films les mieux notés sur IMDb.

- [Préambule](#préambule)
  - [Description de la base de données](#description-de-la-base-de-données)
  - [Installation](#installation)
  - [Lancement de l'application](#lancement-de-lapplication)
- [Préparation et Analyse des Données](#préparation-et-analyse-des-données)
  - [Nettotage des données](#nettotage-des-données)
  - [Analyse des données](#analyse-des-données)
    - [Exploration des données](#exploration-des-données)

## Préambule

### Description de la base de données

La base de données (`./data/imdb_top_1000.csv`) contient les informations suivantes:

| Colonne | Description |
| --- | --- |
| `Poster_link` | lien vers l'affiche du film |
| `Series_Title` | titre de la série |
| `Released_Year` | année de sortie |
| `Certificate` | certification |
| `Runtime` | durée du film |
| `Genre` | genre du film |
| `IMDB_Rating` | note IMDb |
| `Overview` | résumé du film |
| `Meta_score` | score Metacritic |
| `Director` | réalisateur |
| `Star1` | acteur principal 1 |
| `Star2` | acteur principal 2 |
| `Star3` | acteur principal 3 |
| `Star4` | acteur principal 4 |
| `No_of_Votes` | nombre de votes |
| `Gross` | recette |

Celle-ci contient les 1000 films les mieux notés sur IMDb.

### Installation

Vous devez avoir Python 3.6+ installé sur votre machine et virtualenv.

```bash
git clone https://github.com/rphang/AD_IMDb.git
cd AD_IMDb
```

Vous pouvez ensuite installer les dépendances

```bash
virtualenv venv
source venv/bin/activate # Sur Windows: .\venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Lancement de l'application

```bash
python app.py
```

Vous pouvez maintenant accéder au projet sur [http://localhost:8050](http://localhost:8050).

## Préparation et Analyse des Données

### Nettotage des données

Malgré que notre dataset devrait contenir des informations sur les 1000 films les mieux notés sur IMDb, cependant les données sont imparfaites:

Nous allons donc nettoyer notre dataset en **remplaçants les lignes contenant des valeurs manquantes**:

| Colonne | Nombre de valeurs manquantes |
| --- | --- |
| `Certificate` | 101 |
| `Meta_score` | 157 |
| `Gross` | 169 |

- Pour `Meta_score` et `Gross`, nous les remplaçont par la **moyenne** de la colonne.

- Cependant, pour la Certification (`Certificate`) nous remplaçont par défaut par `U` (Ce qui représente des films pour tout public).

### Analyse des données

Nous allons maintenant analyser les données pour en tirer des informations pertinentes.

#### Exploration des données
