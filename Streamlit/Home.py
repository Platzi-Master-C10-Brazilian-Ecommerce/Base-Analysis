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


#Datos importados

#Para el a priori
from mlxtend.preprocessing import TransactionEncoder


translations = pd.read_csv("Streamlit/Datasets/product_category_name_translation.csv")

products =  pd.read_csv("Streamlit/Datasets/olist_products_dataset.csv")

orders =  pd.read_csv("Streamlit/Datasets/olist_orders_dataset.csv")

#Poner los nombres en inglés
products = products.merge(translations, on='product_category_name', how="left")
orders = orders.merge(products[['product_id','product_category_name_english']], on='product_id', how='left')
orders.dropna(inplace=True, subset=['product_category_name_english'])


transactions = orders.groupby("order_id").product_category_name_english.unique()
#Aqui asumimos que solo vaya a haber una compra de la categoria

transactions = transactions.tolist()

counts = [len(transaction) for transaction in transactions]

encoder = TransactionEncoder()


encoder.fit(transactions)

# Transform lists into one-hot encoded array.
onehot = encoder.transform(transactions)

# Convert array to pandas DataFrame.
onehot = pd.DataFrame(onehot, columns = encoder.columns_)

from mlxtend.frequent_patterns import apriori

frequent_itemsets = apriori(onehot, min_support = 0.00001, use_colnames=True)

frequent_itemsets = apriori(onehot, min_support = 0.00001, max_len = 2, use_colnames = True)

from mlxtend.frequent_patterns import association_rules

rules = association_rules(frequent_itemsets, metric = 'confidence', min_threshold = 0.01)

rules = rules[rules['consequent support'] > 0.095]



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
        header=dict(values=list(rules.columns),
                    fill_color='darkblue',
                    align='center'),
        cells=dict(values=[rules.antecedents, rules.consequents, rules.support],
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


