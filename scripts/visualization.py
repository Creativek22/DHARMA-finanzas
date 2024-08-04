import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_summary(summary):
    st.write(summary)

def plot_profitability(most_profitable, least_profitable):
    st.write("Producto más rentable:")
    st.write(most_profitable)
    st.write("Producto menos rentable:")
    st.write(least_profitable)

def plot_trends(trends):
    st.line_chart(trends)
