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

# Converting these fkn columns to numeric
basicsDf['startYear'] = pd.to_numeric(basicsDf['startYear'], errors='coerce')
basicsDf['endYear'] = pd.to_numeric(basicsDf['endYear'], errors='coerce')
basicsDf['runtimeMinutes'] = pd.to_numeric(basicsDf['runtimeMinutes'], errors='coerce')
basicsDf['averageRating'] = pd.to_numeric(basicsDf['averageRating'], errors='coerce').fillna(0)

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(basicsDf.titleType.unique(), 'movie', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = basicsDf[basicsDf.titleType==value]
    # Sort the X axis
    dff = dff.sort_values('startYear')
    return px.scatter(dff, x='startYear', y='averageRating', color='genres', hover_name='primaryTitle')

# K Means test
from sklearn.cluster import KMeans
import numpy as np

# start time
import time
start = time.time()

kmeans = KMeans(n_clusters=3)
kmeans.fit(basicsDf[['startYear', 'averageRating']])
basicsDf['cluster'] = kmeans.predict(basicsDf[['startYear', 'averageRating']])
fig = px.scatter(basicsDf, x='startYear', y='averageRating', color='cluster')
end = time.time()
print('Time taken:', end-start)
fig.show()

if __name__ == '__main__':
    app.run(debug=True)