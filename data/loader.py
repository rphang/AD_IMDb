import pandas as pd
import numpy as np

def getDataset():
    df = pd.read_csv('./data/imdb_top_1000.csv')
    def clean_year(year):
        try:
            return int(year)
        except ValueError:
            return 1995
    
    df['Released_Year'] = df['Released_Year'].apply(clean_year)
    df['Released_Year'] = pd.to_datetime(df['Released_Year'], format='%Y').dt.year
    df["Gross"] = df["Gross"].str.replace(",","")
    df["Gross"] = df["Gross"].replace(np.nan, 0)
    df["Gross"] = df["Gross"].astype(int)
    df['Runtime'] = df['Runtime'].astype(str).str.extract('(\d+)', expand=False)
    df['Runtime'] = pd.to_numeric(df['Runtime'], errors='coerce').fillna(0).astype(int)
    df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].mean())
    df["Gross"] = df["Gross"].replace(0,df['Gross'].mean())
    df['Certificate'] = df['Certificate'].fillna('U')

    return df