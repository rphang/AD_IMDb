from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

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
                        'genres': str # multi valued ("genre1,genre2,...")
                 }
)
reviewsDf = pd.read_csv('./data/title.ratings.tsv',
                        sep='\t',
                        header=0,
                        dtype={
                            'tconst': str,
                            'averageRating': str,
                            'numVotes': str
                        }
)
combinedDf = basicsDf.merge(reviewsDf, on=['tconst'], how='inner')

# Converting these fkn columns to numeric
combinedDf['startYear'] = pd.to_numeric(combinedDf['startYear'], errors='coerce')
combinedDf['endYear'] = pd.to_numeric(combinedDf['endYear'], errors='coerce')
combinedDf['runtimeMinutes'] = pd.to_numeric(combinedDf['runtimeMinutes'], errors='coerce')
combinedDf['averageRating'] = pd.to_numeric(combinedDf['averageRating'], errors='coerce').fillna(0)

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(combinedDf.titleType.unique(), 'movie', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = combinedDf[combinedDf.titleType==value]
    # Sort the X axis
    dff = dff.sort_values('startYear')
    return px.scatter(dff, x='startYear', y='averageRating', color='genres', hover_name='primaryTitle')

if __name__ == '__main__':
    app.run(debug=True)