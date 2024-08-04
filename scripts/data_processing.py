import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def process_data(df):
    # Realiza cualquier procesamiento necesario aquí
    df.columns = [col.strip() for col in df.columns]  # Eliminar espacios en los nombres de columnas
    return df
