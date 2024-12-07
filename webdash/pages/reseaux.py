import pandas as pd
import dash
from dash import dcc, html, Input, Output , callback
import dash_bootstrap_components as dbc
import networkx as nx
import plotly.graph_objects as go
from data.loader import getDataset
# Load Dataset
df = getDataset()
df = df.assign(Genre=df['Genre'].str.split(', ')).explode('Genre')

actors_columns = ['Star1', 'Star2', 'Star3', 'Star4']

# Step 5: Create Dash App
dash.register_page(__name__)

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Réseaux d'IMDb", className="text-center mb-4"), width=12)
    ]),
    html.P("Il est intéressant de voir comment les acteurs et les réalisateurs collaborent ensemble pour créer des films. En utilisant les données d'IMDb, nous pouvons créer des réseaux pour visualiser ces collaborations."),
    html.P("Le premier réseau montre les 50 acteurs les plus populaires jouant dans les mêmes films dans un certain genre. Le deuxième réseau montre les réalisateurs les plus actifs et les acteurs les plus communs avec lesquels ils travaillent."),
    html.H2("Top 50 Collaborations d'Acteurs selon le genre"),
    dbc.Row([
        dbc.Col([
            html.Label("Genre de film:"),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': genre, 'value': genre} for genre in df['Genre'].unique()],
                value='Action'
            ),
            dcc.Graph(
                id='actor-network',
            )
        ], width=12)
    ]),
    html.H2("Réseaux de réalisateurs les plus actifs et des acteurs les plus communs"),
    dbc.Row([
        dbc.Col([
            html.Label("Nombre minimum de films par réalisateur:"),
            dcc.Slider(
                id='min-movies-slider',
                min=2,
                max=14,
                step=1,
                value=2,
                marks={i: str(i) for i in range(2, 14)}
            ),
            dcc.Graph(
                id='movie-network',
            )
        ], width=12)
    ]),
])

# Callbacks
@callback(
    Output('actor-network', 'figure'),
    Input('genre-dropdown', 'value')
)
def actor_network(genre):
    df_copy = df.copy()

    # Filter movies by genre (Movie have multiple genres)
    df_copy = df_copy[df_copy['Genre'].apply(lambda x: genre in x)]

    # Step 1: Extract Top 20 Actors
    actors_df = pd.melt(df_copy, value_vars=actors_columns, value_name='Actor').dropna()
    top_actors = actors_df['Actor'].value_counts().head(50).index.tolist()

    # Step 2: Filter Collaborations Between Top Actors
    collaborations = []
    for _, row in df_copy.iterrows():
        movie_actors = set([row[col] for col in actors_columns if row[col] in top_actors])
        collaborations.extend([(a1, a2) for a1 in movie_actors for a2 in movie_actors if a1 != a2])

    # Create a DataFrame for edges
    edges_df = pd.DataFrame(collaborations, columns=['Actor1', 'Actor2'])
    edges_df = edges_df.groupby(['Actor1', 'Actor2']).size().reset_index(name='Weight')

    # Step 3: Build the Graph
    G = nx.Graph()
    for _, row in edges_df.iterrows():
        G.add_edge(row['Actor1'], row['Actor2'], weight=row['Weight'])

    # Step 4: Generate Plotly Graph from NetworkX Graph
    pos = nx.spring_layout(G, k=0.5, seed=42)  # Layout for nodes
    edge_x = []
    edge_y = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node} ({G.degree[node]} connections)")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=[10 + 3 * G.degree[node] for node in G.nodes()],
            color='#00bfff',
            line_width=2))

    return go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(l=40, r=40, t=40, b=40),
                         xaxis=dict(showgrid=False, zeroline=False),
                         yaxis=dict(showgrid=False, zeroline=False)
                     ))


@callback(
    Output('movie-network', 'figure'),
    Input('min-movies-slider', 'value')
)
def movie_network(min_movies):
    G = nx.Graph()
    df_copy = df.copy()
    # filter Directors with less than min_movies
    df_copy = df_copy.groupby('Director').filter(lambda x: len(x) >= min_movies)
    for _, row in df_copy.iterrows():
        movie = row['Series_Title']
        director = row['Director']
        actors = df_copy.loc[df_copy['Series_Title'] == movie, actors_columns].values[0]
        if director not in G.nodes:
            G.add_node(director, node_type='director')
        for actor in actors:
            if actor not in G.nodes:
                G.add_node(actor, node_type='actor')
            G.add_edge(director, actor, movie=movie)
            
    # Filter nodes based on minimum movies and only keep the Director and Actor nodes
    nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < min_movies and G.nodes[node].get('node_type') == 'director']
    G.remove_nodes_from(nodes_to_remove)
    # Remove actors with less than 2 connection
    nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < 2 and G.nodes[node].get('node_type') == 'actor']
    G.remove_nodes_from(nodes_to_remove)

    pos = nx.spring_layout(G, k=0.5, seed=42)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node + f" ({G.degree[node]} connections)<br>" + "<br>".join([f"- {G.edges[edge]['movie']} - {edge[1]}" for edge in G.edges(node)]) if G.nodes[node].get('node_type') == 'director' 
                         else 
                            node + f" ({G.degree[node]} connections)<br>" + "<br>".join([f"- {G.edges[edge]['movie']} - {edge[1]}" for edge in G.edges(node)]))
        node_color.append('#00bfff' if G.nodes[node].get('node_type') == 'director' else '#ff6347')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            size=[10 + 2 * G.degree[node] for node in G.nodes()],
            color=node_color,
            line_width=2))
    
    return go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))
