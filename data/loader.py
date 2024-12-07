import pandas as pd
import numpy as np

def getDataset():
    # Load dataset
    df = pd.read_csv('./data/imdb_top_1000.csv')
    
    # Clean 'Released_Year' column
    # Remove invalid entries (e.g., 'PG') and fill with a default year
    def clean_year(year):
        try:
            # Convert valid years to integer
            return int(year)
        except ValueError:
            # Replace invalid years with a default value (e.g., 1995)
            return 1995

    df['Released_Year'] = df['Released_Year'].apply(clean_year)
    
    # Convert to datetime format and extract the year
    df['Released_Year'] = pd.to_datetime(df['Released_Year'], format='%Y').dt.year

    # Clean 'Gross' column: Remove commas and convert to integer
    df["Gross"] = df["Gross"].str.replace(",","")
    df["Gross"] = df["Gross"].replace(np.nan, 0)
    df["Gross"] = df["Gross"].astype(int)
    # Clean 'Runtime' column: Extract numeric runtime
    df['Runtime'] = df['Runtime'].astype(str).str.extract('(\d+)', expand=False)
    df['Runtime'] = pd.to_numeric(df['Runtime'], errors='coerce').fillna(0).astype(int)
    
    # Empy lines

    # Remplacing na values in 'Meta_score' and 'Gross' with their columns mean
    df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].mean())
    df["Gross"] = df["Gross"].replace(0,df['Gross'].mean())

    # Remplacing na values in 'Certificate' column with 'U'
    df['Certificate'] = df['Certificate'].fillna('U')

    return df