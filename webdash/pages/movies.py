import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

from data.loader import loadBasics

basicsDf = loadBasics()

dash.register_page(__name__)

genreSet = set()
for genres in basicsDf['genres']:
    for genre in genres:
        genreSet.add(genre)

layout = html.Div([
    html.H1('Movies analytics'),
    html.Br(),
    html.H2('Average number of movies per decade by genre'),
    dcc.Dropdown(
        options=[{'label': genre, 'value': genre} for genre in genreSet],
        value='genres',
        id='dropdown-selection'
    ),
    dcc.Graph(id='graph-content'),
    html.Br(),
    html.H2('Trends of runtimeMinutes over time'),
    dcc.Slider(
        basicsDf['startYear'].min(),
        basicsDf['startYear'].max(),
        step=None,
        value=basicsDf['startYear'].min(),
        marks={str(year): str(year) for year in basicsDf['startYear'].unique()},
        id='year-slider'
    ),
    dcc.Graph(id='runtimeMinutes-trends')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_avg_movie_per_decade(input):
    filteredDf = basicsDf[basicsDf['genres'].apply(lambda x: input in x)]
    filteredDf = filteredDf[filteredDf['startYear'].notna()]
    return px.bar(filteredDf.groupby('startYear').size(), title='Average number of movies per decade', labels={'index': 'Decade', 'value': 'Number of movies'})

@callback(
    Output('runtimeMinutes-trends', 'figure'),
    Input('year-slider', 'value')
)
def update_runtimeMinutes_trends(input):
    filteredDf = basicsDf[basicsDf['startYear'] == input]
    fig = px.scatter(filteredDf, x='runtimeMinutes', y='averageRating', title='Trends of runtimeMinutes over time')
    fig.update_layout(xaxis_title='runtimeMinutes', yaxis_title='Average rating')
    return fig