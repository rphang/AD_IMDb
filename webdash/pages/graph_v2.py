"""import pandas as pd
import networkx as nx
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data.loader import loadNewDataset

# Load Your Dataset
df = loadNewDataset()  # Replace with your dataset path

# Drop rows with missing stars
df = df.dropna(subset=["Star1", "Star2", "Star3", "Star4"])

# Create Graph
G = nx.Graph()

# Add unique edges
for _, row in df.iterrows():
    title = row["Series_Title"]
    stars = set([row["Star1"], row["Star2"], row["Star3"], row["Star4"]])  # Avoid duplicates
    for star in stars:
        G.add_edge(title, star)  # Link series to stars
    for star1 in stars:
        for star2 in stars:
            if star1 != star2:
                G.add_edge(star1, star2)  # Link stars to each other

# Convert Graph to Plotly Scatter Plot
pos = nx.spring_layout(G)  # Layout for graph
edge_x = []
edge_y = []

# Extract edge coordinates
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines"
)

# Extract node coordinates and information
node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    hoverinfo="text",
    text=node_text,
    textposition="top center",
    marker=dict(
        showscale=True,
        colorscale="YlGnBu",
        size=10,
        colorbar=dict(
            thickness=15,
            title="Node Connections",
            xanchor="left",
            titleside="right"
        )
    )
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Graph of Stars and Series Titles (Deduplicated)",
                    titlefont_size=16,
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=0, l=0, r=0, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                ))

# Dash App
dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stars and Series Title Graph", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graph", figure=fig)
        ], width=12)
    ])
])"""