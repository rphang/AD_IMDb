import dash
from dash import dcc, html, Input, Output , callback
import dash_bootstrap_components as dbc
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import DBSCAN
from data.loader import getDataset
from sklearn.decomposition import PCA

# Load Dataset
df = getDataset()
features = df[['Runtime', 'No_of_Votes', 'Gross', 'IMDB_Rating']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)
df['PCA1'] = pca_features[:, 0]
df['PCA2'] = pca_features[:, 1]

# Initialize Dash App
dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Analyse de regroupement des films", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("K-Means Clustering"),
            html.Label("Sélectionnez le nombre de clusters :"),
            dcc.Slider(
                id='kmeans-slider',
                min=2,
                max=10,
                step=1,
                value=3,
                marks={i: str(i) for i in range(2, 11)}
            ),
            dcc.Graph(id='kmeans-cluster-plot')
        ], width=12)
    ]),
    html.Hr(), 
    dbc.Row([
        dbc.Col([
            html.H2("DBSCAN Clustering"),
            html.Label("Sélectionnez les paramètres DBSCAN :"),
            html.Div([
                html.Label("Epsilon (eps):"),
                dcc.Slider(
                    id='dbscan-eps-slider',
                    min=0.1,
                    max=3.0,
                    step=0.1,
                    value=0.5,
                    marks={round(i, 1): str(round(i, 1)) for i in np.arange(0.1, 3.1, 0.5)}
                ),
                html.Label("Min Samples:"),
                dcc.Slider(
                    id='dbscan-min-samples-slider',
                    min=2,
                    max=20,
                    step=1,
                    value=5,
                    marks={i: str(i) for i in range(2, 21)}
                ),
            ]),
            dcc.Graph(id='dbscan-cluster-plot')
        ], width=12)
    ]),
    html.Hr(), 
    dbc.Row([
        dbc.Col([
            html.H2("DBSCAN Clustering avec PCA"),
            html.Label("Sélectionnez les paramètres DBSCAN :"),
            html.Div([
                html.Label("Epsilon (eps):"),
                dcc.Slider(
                    id='dbscan-eps-slider',
                    min=0.1,
                    max=3.0,
                    step=0.1,
                    value=0.5,
                    marks={round(i, 1): str(round(i, 1)) for i in np.arange(0.1, 3.1, 0.5)}
                ),
                html.Label("Min Samples:"),
                dcc.Slider(
                    id='dbscan-min-samples-slider',
                    min=2,
                    max=20,
                    step=1,
                    value=5,
                    marks={i: str(i) for i in range(2, 21)}
                ),
            ]),
            dcc.Graph(id='dbscan-pca-plot')
        ], width=12)
    ])
])
@callback(
    Output('kmeans-cluster-plot', 'figure'),
    Input('kmeans-slider', 'value')
)
def update_kmeans_clusters(n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(scaled_features)
    df['KMeans_Cluster'] = df['KMeans_Cluster'].astype(str)
    fig = px.scatter_3d(
        df,
        x='Runtime',
        y='Gross',
        z='No_of_Votes',
        color='KMeans_Cluster',
        title=f'K-Means Clustering with {n_clusters} Clusters',
        hover_data=['Runtime', 'IMDB_Rating', 'No_of_Votes', 'Gross','Genre']
    )
    return fig

@callback(
    Output('dbscan-cluster-plot', 'figure'),
    [Input('dbscan-eps-slider', 'value'),
    Input('dbscan-min-samples-slider', 'value')]
)
def update_dbscan_clusters(eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df['DBSCAN_Cluster'] = dbscan.fit_predict(scaled_features)
    df['DBSCAN_Cluster'] = df['DBSCAN_Cluster'].apply(lambda x: 'Noise' if x == -1 else str(x))
    fig = px.scatter_3d(
        df,
        x='Runtime',
        y='Gross',
        z='No_of_Votes',
        color='DBSCAN_Cluster',
        title=f'DBSCAN Clustering (eps={eps}, min_samples={min_samples})',
        hover_data=['Runtime', 'IMDB_Rating', 'No_of_Votes', 'Gross', 'Genre']
    )
    return fig

@callback(
    Output('dbscan-pca-plot', 'figure'),
    [Input('dbscan-eps-slider', 'value'),
    Input('dbscan-min-samples-slider', 'value')]
)
def update_dbscan_pca_clusters(eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df['DBSCAN_Cluster'] = dbscan.fit_predict(scaled_features)
    df['DBSCAN_Cluster'] = df['DBSCAN_Cluster'].apply(lambda x: 'Noise' if x == -1 else str(x))

    fig = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color='DBSCAN_Cluster',
        title=f'DBSCAN Clustering with PCA (eps={eps}, min_samples={min_samples})',
        hover_data=['Runtime', 'IMDB_Rating', 'No_of_Votes', 'Gross', 'Genre'] 
    )
    return fig