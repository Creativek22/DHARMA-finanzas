import streamlit as st
import pandas as pd
import base64
import os
import plotly.express as px

# Configurar el tema de Streamlit desde .streamlit/config.toml
st.set_page_config(page_title="Análisis Financiero", layout="centered", initial_sidebar_state="collapsed")

# Mostrar el logo de la empresa centrado y con el tamaño original
logo_path = os.path.join('assets', 'logo.webp')  # Asegúrate de que el logo esté en la carpeta 'assets'
logo_bytes = open(logo_path, "rb").read()
logo_base64 = base64.b64encode(logo_bytes).decode("utf-8")

st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/webp;base64,{logo_base64}">
    </div>
""", unsafe_allow_html=True)

# Título de la Aplicación
st.title('Análisis Financiero')

# Cargar datos directamente desde el archivo CSV actualizado
data_file = 'data/tabla.csv'
df = pd.read_csv(data_file, index_col=0)  # Eliminar la primera columna que numera las filas

# Convertir las columnas de porcentaje a tipo numérico, si son de tipo cadena
for col in df.columns:
    if '%' in col and df[col].dtype == 'object':
        df[col] = pd.to_numeric(df[col].str.replace('%', ''), errors='coerce')

# Redondear los valores a enteros y formatear los porcentajes sin decimales
df = df.round(0)
for col in df.columns:
    if '%' in col:
        df[col] = df[col].astype(int)

# Comprobar si la fila de totales está presente y eliminarla
if 'Total' in df.index:
    df = df.drop('Total')

# Mostrar la tabla de datos inicial
st.dataframe(df)

# Traducción de las columnas estadísticas
stat_translation = {
    'count': 'Recuento',
    'mean': 'Media',
    'std': 'Desviación Estándar',
    'min': 'Mínimo',
    '25%': '25%',
    '50%': 'Mediana',
    '75%': '75%',
    'max': 'Máximo'
}

# Opciones de Análisis
st.markdown("## Opciones de Análisis")
analysis_option = st.selectbox('Selecciona una opción de análisis:', 
                               ('Análisis Financiero Completo', 
                                'Productos de Mayor y Menor Rentabilidad', 
                                'Identificar Patrones o Tendencias'))

# Botón para ejecutar el análisis
execute_button = st.button('Ejecutar Análisis')

# Realizar Análisis solo si se presiona el botón
if execute_button:
    if analysis_option == 'Análisis Financiero Completo':
        summary = df.describe().rename(index=stat_translation).round(0)
        st.markdown("## Análisis Financiero Completo")
        st.dataframe(summary)

        # Mostrar los totales en formato Markdown
        total_kg = df.filter(like='(Kg)').sum().sum()
        total_dollar = df.filter(like='($)').sum().sum()
        st.markdown(f"**Total (Kg):** {total_kg:,.0f}")
        st.markdown(f"**Total ($):** {total_dollar:,.0f}")

        # Preparar datos para el gráfico de Total ($) por Producto
        df_product_total = df[['Enero ($)', 'Febrero ($)', 'Marzo ($)', 'Abril ($)']].sum(axis=1).reset_index()
        df_product_total.columns = ['Producto', 'Total ($)']
        df_product_total = df_product_total[df_product_total['Producto'] != 'Total']

        # Gráfico de Total ($) por Producto
        fig = px.bar(df_product_total, x='Producto', y='Total ($)', title='Total ($) por Producto')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico de Pastel de Total ($) por Producto
        fig_pie = px.pie(df_product_total, names='Producto', values='Total ($)', title='Distribución del Total ($) por Producto')
        st.plotly_chart(fig_pie, use_container_width=True)

    elif analysis_option == 'Productos de Mayor y Menor Rentabilidad':
        profitability = df[['Enero ($)', 'Febrero ($)', 'Marzo ($)', 'Abril ($)']].sum(axis=1).reset_index()
        profitability.columns = ['Producto', 'Total ($)']
        profitability['% Total ($)'] = (profitability['Total ($)'] / profitability['Total ($)'].sum()) * 100

        # Gráfico de barras horizontales de rentabilidad con colores diferenciados para cada producto
        fig_barh = px.bar(profitability, y='Producto', x='Total ($)', orientation='h', title='Rentabilidad por Producto', color='Producto')
        fig_barh.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_barh, use_container_width=True)

    elif analysis_option == 'Identificar Patrones o Tendencias':
        st.markdown("## Identificar Patrones o Tendencias")
        df_kg = df.filter(like='(Kg)')
        df_dollar = df.filter(like='($)')

        # Gráfico de tendencias en Kg
        fig_kg = px.line(df_kg, x=df_kg.index, y=df_kg.columns, title='Tendencias en Kg')
        fig_kg.update_layout(xaxis_title='Mes', yaxis_title='Cantidad (Kg)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_kg, use_container_width=True)

        # Gráfico de tendencias en $
        fig_dollar = px.line(df_dollar, x=df_dollar.index, y=df_dollar.columns, title='Tendencias en $')
        fig_dollar.update_layout(xaxis_title='Mes', yaxis_title='Valor ($)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_dollar, use_container_width=True)

else:
    st.write("Selecciona una opción de análisis y presiona el botón 'Ejecutar Análisis'.")
