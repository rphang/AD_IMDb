import pandas as pd

movieDf = pd.read_csv('./data/title.basics.tsv', 
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
                        'genres': str # multi valued ("genre1,genre2,...")
                 }
)

ratingsDf = pd.read_csv('./data/title.ratings.tsv',
                        sep='\t',
                        header=0,
                        dtype={
                            'tconst': str,
                            'averageRating': str,
                            'numVotes': str
                        }
)

newDf = movieDf[movieDf.titleType.isin(['movie', 'tvSeries', 'tvEpisode'])]
newDf = newDf[newDf.isAdult == '0']
newDf = newDf[newDf.startYear >= '1990']
newDf = newDf[newDf.startYear <= '2026']

print(newDf.titleType.value_counts())

newDf = newDf.merge(ratingsDf, on=['tconst'], how='inner')
#  save into file
newDf.to_csv('./filtered_title.basics.tsv', sep='\t', index=False)