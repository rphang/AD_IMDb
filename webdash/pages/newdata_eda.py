import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import dash
from dash import html, dcc,callback, Input, Output
import dash_bootstrap_components as dbc
from data.loader import getDataset
import plotly.express as px

# Load Dataset
df = getDataset()

df['Genre'] = df['Genre'].fillna('Unknown')  
expanded_df = df.assign(Genre=df['Genre'].str.split(', ')).explode('Genre')
genre_counts = expanded_df['Genre'].value_counts().reset_index() 
genre_counts.columns = ['Genre', 'Count']

numeric_cols = df.select_dtypes(include=['float64', 'int64', 'Int64'])
corr_matrix = numeric_cols.corr()


top_directors = df['Director'].value_counts().reset_index().head(10)
top_directors.columns = ['Director', 'Count']

certificate_counts = df['Certificate'].value_counts().reset_index()
certificate_counts.columns = ['Certificate', 'Count']

df_years_genre = df.dropna(subset=["Released_Year", "Genre"])
df_years_genre["Released_Year"] = pd.to_numeric(df_years_genre["Released_Year"], errors="coerce")  # Ensure Year is numeric
df_years_genre = df_years_genre.dropna(subset=["Released_Year"])
df_years_genre["Released_Year"] = df_years_genre["Released_Year"].astype(int)

genre_split = df["Genre"].str.split(", ").explode()
genre_distribution = genre_split.groupby([df["Released_Year"], genre_split]).size().unstack(fill_value=0)

df_genre_gross = df[["Genre", "Gross"]]  
df_genre_gross["Gross"] = pd.to_numeric(df_genre_gross["Gross"], errors="coerce")  
df_genre_gross = df_genre_gross.dropna(subset=["Gross"]) 

unique_genres = sorted(set(genre.strip() for genres in df['Genre'].dropna() for genre in genres.split(', ')))
unique_genres.insert(0, 'All')
expanded_frame = df_genre_gross.assign(Genre=df_genre_gross["Genre"].str.split(", ")).explode("Genre")

df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
avg_rating_per_year = df.groupby('Released_Year')['IMDB_Rating'].mean().reset_index()
avg_rating_per_year = avg_rating_per_year.dropna().sort_values('Released_Year')

avg_gross_per_year = df.groupby('Released_Year')['Gross'].mean().reset_index()
avg_gross_per_year = avg_gross_per_year.dropna().sort_values('Released_Year')

df_copy = df.copy()

df_copy['Gross'] = df_copy['Gross'].astype(str).str.replace(',', '').astype(float, errors='ignore')  # Convert to numeric
df_copy['No_of_Votes'] = pd.to_numeric(df_copy['No_of_Votes'], errors='coerce')
df_scatter = df_copy[['No_of_Votes', 'Gross']].dropna()  # Drop rows with missing values

dash.register_page(__name__)
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Pairplot Visualization", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Features for Pairplot:"),
            dcc.Dropdown(
                id='pairplot-features',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['float64', 'int64']).columns],
                value=list(df.select_dtypes(include=['float64', 'int64']).columns),
                multi=True,
                placeholder="Select numerical features"
            ),
            html.Button("Generate Pairplot", id="generate-pairplot", n_clicks=0, className="btn btn-primary mt-2"),
            html.Div(id='pairplot-container', className="mt-4")
        ], width=12)
    ]),
    html.Hr(), 
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='top-directors-bar-plot',
                figure=px.bar(
                    top_directors,
                    x='Count',
                    y='Director',
                    orientation='h',
                    title="Top 10 Directors by Number of Movies",
                    labels={'Count': 'Count', 'Director': 'Director'},
                    color_discrete_sequence=px.colors.qualitative.Bold
                ).update_layout(
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=500
                )
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='certificate-bar-plot',
                figure=px.bar(
                    certificate_counts,
                    x='Count',
                    y='Certificate',
                    orientation='h',
                    title="Distribution of Certificates",
                    labels={'Count': 'Count', 'Certificate': 'Certificate'},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                ).update_layout(
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=500
                )
            )
        ], width=6)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H1("Movie Genres Distribution", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='genre-bar-plot')
        ], width=12)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H1("Genre Trends Over the Years", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="genre-trends-plot"),
        ], width=12)
    ]),
    html.Hr(), 
    dbc.Row([
        dbc.Col(html.H1("Average Gross Revenue by Genre", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="average-gross-plot") 
        ], width=12)
    ]),
    html.Hr(), 

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='correlation-heatmap',
                figure=px.imshow(
                    corr_matrix,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    color_continuous_scale='Viridis'
                ).update_layout(margin=dict(l=40, r=40, t=40, b=40))
            )
        ], width=12)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H1("Correlation Between Votes and Gross", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='votes-gross-scatter',
                figure=px.scatter(
                    df_scatter,
                    x='No_of_Votes',
                    y='Gross',
                    title="Correlation Between Number of Votes and Gross",
                    labels={'No_of_Votes': 'Number of Votes', 'Gross': 'Gross Revenue'},
                    trendline='ols',  
                    color_discrete_sequence=['#636EFA'] 
                ).update_layout(
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=600
                )
            )
        ], width=12)
    ]),
    html.Hr(), 
        dbc.Row([
        dbc.Col(html.H1("Average IMDb Rating and Gross Per Year (By Genre)", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Genre:"),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': genre, 'value': genre} for genre in unique_genres],
                value='All', 
                multi=False,
                clearable=False
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='avg-imdb-rating')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='avg-gross')
        ], width=6)
    ])
])

@callback(
    Output('pairplot-container', 'children'),
    Input('generate-pairplot', 'n_clicks'),
    Input('pairplot-features', 'value')
)
def update_pairplot(n_clicks, selected_features):
    if n_clicks > 0 and selected_features:
        sns.set(style="whitegrid")
        plt.style.use('Solarize_Light2')
        pairplot = sns.pairplot(df[selected_features])
        buf = io.BytesIO()
        pairplot.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': '100%'})

    return html.Div("Please select features and click Generate Pairplot.", style={'color': 'red', 'font-weight': 'bold'})




@callback(
    Output('genre-bar-plot', 'figure'),
    Input('genre-bar-plot', 'id')
)
def update_genre_plot(_):
    fig = px.bar(
        genre_counts,
        x='Count',
        y='Genre',
        orientation='h',
        title="Distribution of Movie Genres",
        color='Genre', 
        labels={'Count': 'Count', 'Genre': 'Genre'}
    )
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=80))
    return fig


@callback(
    Output("genre-trends-plot", "figure"),
    Input("genre-trends-plot", "id") 
)
def update_genre_trends_plot(_):
    total_counts = genre_distribution.sum()
    top_genres = total_counts.nlargest(5).index
    top_genre_distribution = genre_distribution[top_genres]
    fig = px.line(
        top_genre_distribution,
        x=top_genre_distribution.index,
        y=top_genre_distribution.columns,
        labels={"value": "Count", "index": "Year"},
        title="Count of Movies for Each Genre Over the Years (Top 5)"
    )

    fig.update_layout(
        legend_title="Genre",
        xaxis_title="Year",
        yaxis_title="Count",
        legend=dict(orientation="v", yanchor="top", y=0.75,xanchor="left", x=1.05),
        margin=dict(l=20, r=120, t=40, b=20)
    )

    return fig


@callback(
    Output("average-gross-plot", "figure"),
    Input("average-gross-plot", "id") 
)
def update_average_gross_plot(_):
    average_gross = expanded_frame.groupby("Genre")["Gross"].mean().sort_values(ascending=False)
    fig = px.bar(
        average_gross,
        x=average_gross.index,
        y=average_gross.values,
        labels={"x": "Genre", "y": "Average Gross Revenue"},
        title="Average Gross Revenue for Each Genre",
        color=average_gross.index,
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Gross Revenue",
        xaxis_tickangle=70, 
        margin=dict(l=20, r=20, t=40, b=100) 
    )
    return fig


@callback(
    [Output('avg-imdb-rating', 'figure'),
    Output('avg-gross', 'figure')],
    [Input('genre-dropdown', 'value')]
)
def update_graphs(selected_genre):
    if selected_genre == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Genre'].str.contains(selected_genre, na=False)]
    avg_rating_per_year = (
        filtered_df.groupby('Released_Year')['IMDB_Rating'].mean().reset_index()
    ).dropna().sort_values('Released_Year')

    avg_gross_per_year = (
        filtered_df.groupby('Released_Year')['Gross'].mean().reset_index()
    ).dropna().sort_values('Released_Year')
    rating_fig = px.bar(
        avg_rating_per_year,
        x='Released_Year',
        y='IMDB_Rating',
        title=f'Average IMDb Rating Over the Years ({selected_genre})',
        labels={'Released_Year': 'Year', 'IMDB_Rating': 'Average IMDb Rating'},
        color_discrete_sequence=['#636EFA']
    ).update_layout(xaxis=dict(tickangle=45), height=500)
    gross_fig = px.bar(
        avg_gross_per_year,
        x='Released_Year',
        y='Gross',
        title=f'Average Gross Per Year ({selected_genre})',
        labels={'Released_Year': 'Year', 'Gross': 'Average Gross Revenue'},
        color_discrete_sequence=['#EF553B']
    ).update_layout(xaxis=dict(tickangle=45), height=500)
    return rating_fig, gross_fig