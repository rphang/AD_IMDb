import pandas as pd
import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from data.loader import getDataset
# Load Dataset
df = getDataset()


df['Genre'] = df['Genre'].fillna('Unknown') 
df['IMDB_Rating'] = pd.to_numeric(df['IMDB_Rating'], errors='coerce')
dash.register_page(__name__, order=0, path='/')

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Filtrer les films par note et genre", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Sélectionnez le(s) genre(s) :"),
            dcc.Dropdown(
                id='genre-filter',
                options=[{'label': genre, 'value': genre} for genre in df['Genre'].str.split(', ').explode().unique()],
                multi=True,
                placeholder="Sélectionnez un ou plusieurs genres"
            ),
        ], width=6),
        dbc.Col([
            html.Label("Sélectionnez la plage de notes IMDb :"),
            dcc.RangeSlider(
                id='rating-filter',
                min=df['IMDB_Rating'].min(),
                max=df['IMDB_Rating'].max(),
                step=0.1,
                value=[df['IMDB_Rating'].min(), df['IMDB_Rating'].max()],
                marks={i: str(i) for i in range(int(df['IMDB_Rating'].min()), int(df['IMDB_Rating'].max()) + 1)}
            ),
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col(html.H3("Films filtrés :", className="text-center mt-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(id='filtered-results', className="mt-4"), width=12
        )
    ])
])



@callback(
    Output('filtered-results', 'children'),
    [Input('genre-filter', 'value'), Input('rating-filter', 'value')]
)
def update_filtered_results(selected_genres, rating_range):
    # Filter by Rating Range
    filtered_df = df[(df['IMDB_Rating'] >= rating_range[0]) & (df['IMDB_Rating'] <= rating_range[1])]

    # Apply Multi-Genre Filter
    if selected_genres:
        # Check if all selected genres exist in the `Genre` column
        filtered_df = filtered_df[
            filtered_df['Genre'].apply(lambda genres: all(genre in genres.split(', ') for genre in selected_genres))
        ]

    # If no results, show message
    if filtered_df.empty:
        return html.Div("No movies match the selected criteria.", style={'color': 'red', 'font-weight': 'bold'})

    # Select relevant columns for display
    filtered_df = filtered_df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

    # Create the table
    return dbc.Table.from_dataframe(
        filtered_df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True
    )