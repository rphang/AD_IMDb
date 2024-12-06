"""import pandas as pd
import dash
from dash import dcc, html, Input, Output , callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data.loader import loadBasics
from itertools import chain

# Load Dataset
df = loadBasics()

# Clean Data (Example: Handle Missing Values)
df = df.dropna(subset=['averageRating', 'runtimeMinutes'])

# Initialize Dash App
dash.register_page(__name__)

# Layout
unique_genres = set(chain.from_iterable(df['genres']))
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Movie Dataset EDA", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Feature for Distribution:"),
            dcc.Dropdown(
                id='dist-feature',
                options=[
                    {'label': 'Average Rating', 'value': 'averageRating'},
                    {'label': 'Runtime (Minutes)', 'value': 'runtimeMinutes'},
                    {'label': 'Number of Votes', 'value': 'numVotes'}
                ],
                value='averageRating',
                clearable=False
            ),
            dcc.Graph(id='dist-plot')
        ], width=6),
        dbc.Col([
            html.Label("Select Genre:"),
            dcc.Dropdown(
                id='genre-filter',
                options=[{'label': genre, 'value': genre} for genre in unique_genres],
                value=None,
                multi=True,
                placeholder="Filter by Genre"
            ),
            dcc.Graph(id='scatter-plot')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Runtime vs. Rating Over Years:"),
            dcc.Slider(
                id='year-slider',
                min=df['startYear'].min(),
                max=df['startYear'].max(),
                step=1,
                value=df['startYear'].min(),
                marks={year: str(year) for year in range(df['startYear'].min(), df['startYear'].max()+1, 10)}
            ),
            dcc.Graph(id='line-plot')
        ], width=12)
    ])
])

# Callbacks
@callback(
    Output('dist-plot', 'figure'),
    Input('dist-feature', 'value')
)
def update_distribution(feature):
    fig = px.histogram(df, x=feature, nbins=30, title=f'Distribution of {feature}')
    return fig

@callback(
    Output('scatter-plot', 'figure'),
    [Input('genre-filter', 'value')]
)
def update_scatter(selected_genres):
    filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(item for item in selected_genres if item in x))]
    fig = px.scatter(filtered_df, x='runtimeMinutes', y='averageRating', color='genres',
                    title='Runtime vs. Rating by Genre', hover_data=['titleType'])
    return fig

@callback(
    Output('line-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def update_line(year):
    year_df = df[df['startYear'] == year]
    fig = px.scatter(year_df, x='runtimeMinutes', y='averageRating', color='genres',
                    title=f'Runtime vs. Rating for Year {year}')
    return fig"""