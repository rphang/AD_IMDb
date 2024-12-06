import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import networkx as nx
import plotly.graph_objects as go
from data.loader import loadNewDataset
# Load Dataset
df = loadNewDataset()
df_copy = df.copy()

# Step 1: Extract Top 20 Actors
actors_columns = ['Star1', 'Star2', 'Star3', 'Star4']
actors_df = pd.melt(df_copy, value_vars=actors_columns, value_name='Actor').dropna()
top_actors = actors_df['Actor'].value_counts().head(20).index.tolist()

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
        size=[10 + G.degree[node] for node in G.nodes()],
        color='#00bfff',
        line_width=2))

# Step 5: Create Dash App
dash.register_page(__name__)

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Actor Collaboration Network", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='actor-network',
                figure=go.Figure(data=[edge_trace, node_trace],
                                 layout=go.Layout(
                                     title='Top 20 Actor Collaborations',
                                     showlegend=False,
                                     hovermode='closest',
                                     margin=dict(l=40, r=40, t=40, b=40),
                                     xaxis=dict(showgrid=False, zeroline=False),
                                     yaxis=dict(showgrid=False, zeroline=False)
                                 ))
            )
        ], width=12)
    ])
])