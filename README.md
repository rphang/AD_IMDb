# Top 1000 des Films basés sur le score IMDb

Ce projet a pour but de créer une application web permettant d'appliquer de l'analyse de données les 1000 films les mieux notés sur IMDb.

- [Préambule](#préambule)
  - [Description de la base de données](#description-de-la-base-de-données)
  - [Installation](#installation)
  - [Lancement de l'application](#lancement-de-lapplication)
- [Préparation et Analyse des Données](#préparation-et-analyse-des-données)
  - [Nettotage des données](#nettotage-des-données)
  - [Analyse des données](#analyse-des-données)
    - [Évolution du nombre de films produits pour chaque genre parmi les 5 genres les plus fréquents](#évolution-du-nombre-de-films-produits-pour-chaque-genre-parmi-les-5-genres-les-plus-fréquents)
    - [Genre avec le plus grand revenu](#genre-avec-le-plus-grand-revenu)
    - [Corrélation entre le nombre de votes et le budget](#corrélation-entre-le-nombre-de-votes-et-le-budget)

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

- Nous avons égalements des champs contenants plusieurs valeurs séparées par des virgules, l'étape de les splits est fait au moment de l'usage de ces données. (Ex: `Genre`)

### Analyse des données

Nous allons maintenant analyser les données pour en tirer des informations pertinentes. Cet application Dash nous permet de visualiser les données de manière interactive. Voici quelques points clés:

- **EDA** (Exploratory Data Analysis): Analyse et visualisation de l'ensemble de données.
- **Network Mining**: Analyse des relations entre les acteurs et les réalisateurs.
- **Clustering et Classification**: Regroupement des films en fonction de leurs caractéristiques. (Durée, Nombre de votes, revenus, etc.)

## Top 10 des réalisateurs par nombre de films :
-   Alfred Hitchcock et Steven Spielberg dominent la liste avec le plus grand nombre de films.

## Répartition des certificats :
- Le graphique montre une prédominance des certificats "U" (Universel, tous publics), suivis de "A" (Adultes) et "UA" (Universal - Adultes avec supervision). Les certificats américains comme "PG" (Surveillance parentale) et "R" (Restreint) sont moins fréquents, indiquant une majorité de films adaptés à un large public.

#### Évolution du nombre de films produits pour chaque genre parmi les 5 genres les plus fréquents

La production de films a considérablement augmenté dans presque tous les genres après 1970. Cette croissance est probablement due à l'expansion des industries cinématographiques et à la demande croissante du public.

On observe également une forte augmentation des films de genre Drame, ce qui peut être interprété comme une réponse à une demande accrue pour ce type de contenu. Cela a généré des revenus significatifs pour ce genre.

#### Genre avec le plus grand revenu

Le genre "Aventure" a généré le revenu brut moyen le plus élevé par film, suivi par "Science-Fiction" et "Action". Les comédies musicales ont eu le revenu brut moyen le plus bas. Ces résultats vont à l'encontre de la distribution des films par genre, car nous avons vu que les drames étaient les plus produits suivis par les comédies.

#### Corrélation entre le nombre de votes et le budget

Le nombre de votes semble être un bon indicateur de la popularité d'un film, ce qui contribue souvent à des revenus bruts plus élevés. Cependant, ce n'est pas une règle absolue, car certains films très votés n'ont pas généré autant de revenus, probablement en raison de leur mode de diffusion ou de leur budget initial.

- **Indicateur de popularité**: Un nombre élevé de votes indique généralement une popularité accrue.
- **Revenus bruts**: Les films populaires tendent à générer plus de revenus.
- **Exceptions**: Certains films très votés peuvent ne pas avoir des revenus élevés en raison de:
  - Mode de diffusion
  - Budget initial

## revenu brut moyenne :
- On observe une augmentation générale des revenus bruts moyens au fil des décennies, avec des pics significatifs autour des années 1980 et 2020, indiquant des périodes où des films particulièrement lucratifs ont été produits. Cette tendance peut refléter des budgets de production croissants, une hausse des prix des billets, ou des succès commerciaux majeurs au cours de ces périodes

## Réseaux - Top 50 Collaborations d'acteurs selon le genre

Nous pouvons observer par le biais de ce réseaux des communautées de collaborations d'acteurs distinctes selon le genre. Par exemple, les acteurs issues de blockbusters sont souvent interconnectés entre eux (comme les acteurs de la saga du Seigneur des Anneaux, ou de la saga Marvel dans la catégorie Action). Cependant, dans le cas du genre Drama, nous pouvons observer des collaborations plus diversifiées, avec des acteurs interconnectés entre eux provenant de films différents mais nous pouvons déterminer des acteurs importants qui sont des ponts entre ces communautées tel que Brad Pitt, Al Pacino, Robert De Niro, Christian Bale, Morgan Freeman ayant un degré de centralité élevé montrant leur importance dans l'industrie cinématographique et du genre.

## Clustering - Classification des films

Étant donné la faible distance inter-clusters, cela indique que les films sont très similaires entre eux, ce qui peut s'expliquer par le fait que le dataset regroupe les 1000 meilleurs films selon IMDb. Cela est clairement visible dans le graphique de DBSCAN avec PCA, où l'on observe une forte densité de points concentrés dans une même région.
