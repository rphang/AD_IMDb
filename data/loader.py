import pandas as pd

def loadBasics(cleaning=True, normalize=True):
    basicsDf = pd.read_csv('./data/title.basics.tsv', 
                 sep='\t',
                 header=0,
                 dtype={
                        'tconst': str,
                        'titleType': str,
                        'primaryTitle': str,
                        'originalTitle': str,
                        'isAdult': str,
                        'startYear': str,
                        'endYear': str,
                        'runtimeMinutes': str,
                        'genres': str
                 }
    )
    
    if not cleaning:
        return basicsDf
    
    basicsDf['startYear'] = pd.to_numeric(basicsDf['startYear'], errors='coerce')
    basicsDf['endYear'] = pd.to_numeric(basicsDf['endYear'], errors='coerce')
    basicsDf['runtimeMinutes'] = pd.to_numeric(basicsDf['runtimeMinutes'], errors='coerce')
    basicsDf['averageRating'] = pd.to_numeric(basicsDf['averageRating'], errors='coerce').fillna(0)
    basicsDf['genres'] = basicsDf['genres'].str.split(',')
    
    return basicsDf