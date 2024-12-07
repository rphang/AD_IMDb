import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import dash
from dash import html, dcc,callback, Input, Output
import dash_bootstrap_components as dbc
from data.loader import loadNewDataset
import plotly.express as px

# Load Dataset
df = loadNewDataset()

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



df_years_genre = df.dropna(subset=["Released_Year", "Genre"])
df_years_genre["Released_Year"] = pd.to_numeric(df_years_genre["Released_Year"], errors="coerce")  # Ensure Year is numeric
df_years_genre = df_years_genre.dropna(subset=["Released_Year"])
df_years_genre["Released_Year"] = df_years_genre["Released_Year"].astype(int)

# Split Genre into multiple rows if there are multiple genres per movie
genre_split = df["Genre"].str.split(", ").explode()

# Group by year and genre
genre_distribution = genre_split.groupby([df["Released_Year"], genre_split]).size().unstack(fill_value=0)




# Preprocessing: Handle missing values and expand Genre column
df_genre_gross = df.dropna(subset=["Genre", "Gross"])  # Drop rows with missing genres or gross revenue
df_genre_gross["Gross"] = pd.to_numeric(df_genre_gross["Gross"], errors="coerce")  # Ensure Gross is numeric
df_genre_gross = df_genre_gross.dropna(subset=["Gross"])  # Drop rows with non-numeric Gross

# Split Genre into multiple rows if movies belong to multiple genres
expanded_frame = df_genre_gross.assign(Genre=df_genre_gross["Genre"].str.split(", ")).explode("Genre")



df_copy = df.copy()

df_copy['Gross'] = df_copy['Gross'].astype(str).str.replace(',', '').astype(float, errors='ignore')  # Convert to numeric
df_copy['No_of_Votes'] = pd.to_numeric(df_copy['No_of_Votes'], errors='coerce')
df_scatter = df_copy[['No_of_Votes', 'Gross']].dropna()  # Drop rows with missing values

dash.register_page(__name__)
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
        dbc.Col(html.H1("Genre Trends Over the Years", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="genre-trends-plot"),
        ], width=12)
    ]),
    html.Hr(),  # Separator
    dbc.Row([
        dbc.Col(html.H1("Average Gross Revenue by Genre", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="average-gross-plot")  # Placeholder for the plot
        ], width=12)
    ]),
    html.Hr(),  # Separator

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
    html.Hr(),  # Separator
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
                    trendline='ols',  # Add a trendline to visualize the correlation
                    color_discrete_sequence=['#636EFA']  # Customize the color
                ).update_layout(
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=600
                )
            )
        ], width=12)
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
        color='Genre', 
        labels={'Count': 'Count', 'Genre': 'Genre'}
    )
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=80))
    return fig


@callback(
    Output("genre-trends-plot", "figure"),
    Input("genre-trends-plot", "id")  # Trigger callback on load
)
def update_genre_trends_plot(_):
    # Get total count of movies for each genre across all years
    total_counts = genre_distribution.sum()

    top_genres = total_counts.nlargest(5).index

    # Create a dataframe for the top genres
    top_genre_distribution = genre_distribution[top_genres]

    # Create a line plot using Plotly
    fig = px.line(
        top_genre_distribution,
        x=top_genre_distribution.index,
        y=top_genre_distribution.columns,
        labels={"value": "Count", "index": "Year"},
        title="Count of Movies for Each Genre Over the Years (Top 5)"
    )

    # Update the layout for better appearance
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
    Input("average-gross-plot", "id")  # Trigger callback on load
)
def update_average_gross_plot(_):
    # Calculate the average gross revenue for each genre
    average_gross = expanded_frame.groupby("Genre")["Gross"].mean().sort_values(ascending=False)

    # Create a bar plot using Plotly
    fig = px.bar(
        average_gross,
        x=average_gross.index,
        y=average_gross.values,
        labels={"x": "Genre", "y": "Average Gross Revenue"},
        title="Average Gross Revenue for Each Genre",
        color=average_gross.index,
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Gross Revenue",
        xaxis_tickangle=70,  # Rotate x-axis labels for readability
        margin=dict(l=20, r=20, t=40, b=100)  # Add extra space for rotated labels
    )

    return fig