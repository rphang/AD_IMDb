import pandas as pd

"""def loadBasics(cleaning=True, normalize=True):
    basicsDf = pd.read_csv('./data/title.basics.tsv', 
                sep='\t',
                header=0,
                dtype={
                        'tconst': str,
                        'titleType': str,
                        'primaryTitle': str,
                        'originalTitle': str,
                        'isAdult': str,
                        'startYear': str,
                        'endYear': str,
                        'runtimeMinutes': str,
                        'genres': str
                 }
    )
    
    if not cleaning:
        return basicsDf
    
    basicsDf['startYear'] = pd.to_numeric(basicsDf['startYear'], errors='coerce')
    basicsDf['endYear'] = pd.to_numeric(basicsDf['endYear'], errors='coerce')
    basicsDf['runtimeMinutes'] = pd.to_numeric(basicsDf['runtimeMinutes'], errors='coerce')
    basicsDf['averageRating'] = pd.to_numeric(basicsDf['averageRating'], errors='coerce').fillna(0)
    basicsDf['genres'] = basicsDf['genres'].str.split(',')
    basicsDf = basicsDf.dropna()
    
    return basicsDf"""

def loadNewDataset():
    # Load dataset
    df = pd.read_csv('./data/imdb_top_1000.csv')
    df_copy = df.copy()
    
    # Check for missing values
    missing_values = df_copy.isnull().sum()
    
    # Fill missing values in 'Meta_score' and 'Gross' with 0
    df_copy['Meta_score'].fillna(0, inplace=True)
    df_copy['Gross'].fillna(0, inplace=True)
    
    # Clean 'Released_Year' column
    # Remove invalid entries (e.g., 'PG') and fill with a default year
    def clean_year(year):
        try:
            # Convert valid years to integer
            return int(year)
        except ValueError:
            # Replace invalid years with a default value (e.g., 1995)
            return 1995

    df_copy['Released_Year'] = df_copy['Released_Year'].apply(clean_year)
    
    # Convert to datetime format and extract the year
    df_copy['Released_Year'] = pd.to_datetime(df_copy['Released_Year'], format='%Y').dt.year

    # Clean 'Gross' column: Remove commas and convert to integer
    df_copy['Gross'] = df_copy['Gross'].astype(str).str.replace(',', '').astype('Int64', errors='ignore')
    
    # Clean 'Runtime' column: Extract numeric runtime
    df_copy['Runtime'] = df_copy['Runtime'].astype(str).str.extract('(\d+)', expand=False)
    df_copy['Runtime'] = pd.to_numeric(df_copy['Runtime'], errors='coerce').fillna(0).astype(int)
    
    return df_copy