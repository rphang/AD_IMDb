# IMDb - The big analysis.

Yup.

## Installation

You need to have Python 3.6+ installed on your machine and virtualenv.

## Setting up the environment
```bash
virtualenv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Running the project
```bash
python app.py
```

You can now access the project on [http://localhost:8050](http://localhost:8050).


# Context

We have a dataset of movies, actors & ratings

# Cleaning

- delete XXX
- filters type ['movie', 'tvSeries', 'tvEpisode']

# EDA

- pie charts by category, type, etc

- average movie length by decade

- average producted movies by year

- table of top 10 actors by number of movies

- table of top 10 directors by number of movies

- table of top 10 genres by number of movies

- table of top 10 genres by average rating

- evolution of runtime over time

# Network

- Average movies directed by a director


# Cluster

We can build a network of actors and movies. 
We can then use clustering algorithms to find:

- groups of actors that have worked together in the past