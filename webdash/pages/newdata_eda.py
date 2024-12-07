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

dash.register_page(__name__)
df['Genre'] = df['Genre'].fillna('Unknown')  # Handle missing genres
expanded_df = df.assign(Genre=df['Genre'].str.split(', ')).explode('Genre')  # Split and expand genres
genre_counts = expanded_df['Genre'].value_counts().reset_index()  # Count genres
genre_counts.columns = ['Genre', 'Count']

# Select Numeric Features
# Select only numeric columns for correlation
numeric_cols = df.select_dtypes(include=['float64', 'int64', 'Int64'])

# Compute the correlation matrix
corr_matrix = numeric_cols.corr()


top_directors = df['Director'].value_counts().reset_index().head(10)
top_directors.columns = ['Director', 'Count']


certificate_counts = df['Certificate'].value_counts().reset_index()
certificate_counts.columns = ['Certificate', 'Count']

# Layout
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
    html.Hr(),  # Separator
    dbc.Row([
        dbc.Col(html.H1("Movie Genres Distribution", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='genre-bar-plot')
        ], width=12)
    ]),
    html.Hr(),  # Separator
dbc.Row([
        dbc.Col(html.H1("Correlation Heatmap", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='correlation-heatmap',
                figure=px.imshow(
                    corr_matrix,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    color_continuous_scale='RdBu',
                    title="Correlation Heatmap"
                ).update_layout(margin=dict(l=40, r=40, t=40, b=40))
            )
        ], width=12)
    ]),
    html.Hr(),  # Separator
    dbc.Row([
        # Column 1: Top Directors
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

        # Column 2: Certificate Distribution
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
    ])
])

# Callback to Generate Pairplot
@callback(
    Output('pairplot-container', 'children'),
    Input('generate-pairplot', 'n_clicks'),
    Input('pairplot-features', 'value')
)
def update_pairplot(n_clicks, selected_features):
    if n_clicks > 0 and selected_features:
        # Generate Pairplot
        sns.set(style="whitegrid")
        plt.style.use('Solarize_Light2')
        pairplot = sns.pairplot(df[selected_features])
        
        # Save Plot to a Bytes Buffer
        buf = io.BytesIO()
        pairplot.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        # Return the Image in Dash
        return html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': '100%'})

    return html.Div("Please select features and click Generate Pairplot.", style={'color': 'red', 'font-weight': 'bold'})




@callback(
    Output('genre-bar-plot', 'figure'),
    Input('genre-bar-plot', 'id')  # Trigger once on load
)
def update_genre_plot(_):
    # Create Bar Plot
    fig = px.bar(
        genre_counts,
        x='Count',
        y='Genre',
        orientation='h',
        title="Distribution of Movie Genres",
        color='Genre',  # Assign color dynamically by genre
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'Count': 'Count', 'Genre': 'Genre'}
    )
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))
    return fig
