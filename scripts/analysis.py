import pandas as pd

def financial_analysis(df):
    # Análisis financiero completo
    summary = df.describe()
    return summary

def product_profitability(df):
    # Identificar productos de mayor y menor rentabilidad
    profitability = df[['Producto', 'Total ($)', '% Total ($)']]
    most_profitable = profitability.loc[profitability['% Total ($)'].idxmax()]
    least_profitable = profitability.loc[profitability['% Total ($)'].idxmin()]
    return most_profitable, least_profitable

def identify_patterns(df):
    # Identificar patrones o tendencias
    trends = df.groupby('Producto').mean()
    return trends
