#Librerias usadas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from urllib.request import urlopen


import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

# Configuración de la pagina
st.set_page_config(page_title="Bussines Intelligence Team",page_icon="📈",layout="wide")


#Datos importados

#Para el a priori
from mlxtend.preprocessing import TransactionEncoder


translations = 

products = 

orders = 







# Presentación de filas

A, B, C = st.columns(3)

A.image(Image.open("Streamlit/Images/PM_logo.png"))

with C:
    st.markdown('''# Platzi Master Cohort 10
    Bussines Intelligence Team
    - Julián Castro     - Ricardo Escamilla
    - Emmanuel Escobar  - Marco Rocha
    - Juan Rincon       - Robert Barrios
    ''')

with B:
    st.text("MIMIM")


#-------------------------------------------------------#

D,E = st.columns(2)

with D:
    D.markdown("Papel del BI")
    D.header("Analisis de mercado")
with E:
    E.markdown("")


#---------------------------------------------------------#

G, H, I = st.columns(3)

st.header("Paretos Law")

with G:
    G.markdown("pass")

with H:
    pareto_code = ""
    H.code(pareto_code, language="Python")

with I: 
    I.markdown("conclusiones")

#---------------------------------------------------------#

J, K ,L = st.columns(3)


with J:
    st.markdown('Regla de asociación')
    bar7 = go.Figure(data=[go.Table(
        header=dict(values=list(churn.columns),
                    fill_color='darkblue',
                    align='center'),
        cells=dict(values=[churn.Orders, churn.Customers, churn.Percentage],
                fill_color='DarkSlateBlue',
                align='center'))])

    J.write(bar7)
    

#---------------------------------------------------------#

st.header("Maps")

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) 

option = st.selectbox(
     'Seleccionar variable',
     ('Count products', 'Payments products', 'percapita'))

if option == "Purchases by state":

    st.header("Número de compras por estado")
    HtmlFile = open("Streamlit/Geoespatial-Drafts/count.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

elif option == "Average amount of money spent per state": 

    st.header("Media de dinero gastado por estado") 
    HtmlFile = open("Streamlit/Geoespatial-Drafts/payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

else:
    st.header("PIB Percapita)")
    HtmlFile = open("Streamlit/Geoespatial-Drafts/percapitamap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)


