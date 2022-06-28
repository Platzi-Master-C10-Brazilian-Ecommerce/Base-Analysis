#Librerias usadas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from urllib.request import urlopen
import mlxtend


import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

# Configuración de la pagina
st.set_page_config(page_title="Bussines Intelligence Team",page_icon="📈",layout="wide")


# Segmentación de mercado

customers = pd.read_csv("Streamlit/Datasets/olist_customers_dataset.csv")
sellers = pd.read_csv("Streamlit/Datasets/olist_sellers_dataset.csv")
orders_reviews = pd.read_csv("Streamlit/Datasets/olist_order_reviews_dataset.csv")
order_items = pd.read_csv("Streamlit/Datasets/olist_order_items_dataset.csv")
products = pd.read_csv("Streamlit/Datasets/olist_products_dataset.csv")
geolocation = pd.read_csv("Streamlit/Datasets/olist_geolocation_dataset.csv")
category_name_translation = pd.read_csv("Streamlit/Datasets/product_category_name_translation.csv")
orders = pd.read_csv("Streamlit/Datasets/olist_orders_dataset.csv")
orders_payments = pd.read_csv("Streamlit/Datasets/olist_order_payments_dataset.csv")


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
    st.title("Bussines Intelligence")
    st.markdown("")


#-------------------------------------------------------#


#---------------------------------------------------------#

st.header("Maps")

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) 

option = st.selectbox(
     'Seleccionar variable',
     ('Purchases by state', 'Average amount of money spent per states', 'percapita'))

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


