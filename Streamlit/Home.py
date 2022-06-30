#Librerias usadas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from urllib.request import urlopen
import mlxtend
from psycopg2 import DatabaseError
from sqlalchemy import create_engine


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

B.image(Image.open("Streamlit/Images/PM_logo.png"))

with C:
    st.markdown('''# Platzi Master Cohort 10
    Bussines Intelligence Team
    - Julián Castro     - Ricardo Escamilla
    - Emmanuel Escobar  - Marco Rocha
    - Juan Rincon       - Robert Barrios
    ''')

with A:
    st.title("Bussines Intelligence")
    st.markdown("Conocimiento del negocio para tomar buenas desiciones basadas en datos")

st.markdown("***")

#-------------------------------------------------------#

# Sobre Brasil

engine = create_engine('postgresql://usuario_consulta:platzicohort10@platzicohort10.cig2rbjhhqmz.us-east-1.rds.amazonaws.com/Brazilian_e_commerce')
with engine.connect() as con:
  rs = con.execute("SELECT * FROM olist_geolocation_dataset") # query que vamos a realizar
  df = pd.DataFrame(rs.fetchall()) # lectura de las filas, hay mas opciones
  df.columns = rs.keys() # asignar al nombre de las columnas del dataframe los nombres de las columnas de la tabla

payments = pd.read_sql_query("SELECT * FROM olist_order_payments_dataset", engine) # Primer argumento es el query, segundo es el engine
reviews = pd.read_sql_query("SELECT * FROM olist_order_reviews_dataset", engine)
orders = pd.read_sql_query("SELECT * FROM olist_orders_dataset", engine)
products = pd.read_sql_query("SELECT * FROM olist_products_dataset", engine)
sellers = pd.read_sql_query("SELECT * FROM olist_sellers_dataset", engine)
category = pd.read_sql_query("SELECT * FROM product_category_name_translation", engine)
geolocation = pd.read_sql_query("SELECT * FROM olist_geolocation_dataset", engine)
customers = pd.read_sql_query("SELECT * FROM olist_order_customers_dataset", engine)
items = pd.read_sql_query("SELECT * FROM olist_order_items_dataset", engine)
states = pd.read_sql_query("SELECT * FROM states", engine)
regions = pd.read_sql_query("SELECT * FROM regions", engine)
cities = pd.read_sql_query("SELECT * FROM cities", engine)
new_customers = pd.read_sql_query("SELECT * FROM new_customers", engine)
new_geolocation = pd.read_sql_query("SELECT * FROM new_geolocation", engine)
new_sellers = pd.read_sql_query("SELECT * FROM new_sellers", engine)
poblacion_brasil = pd.read_sql_query("SELECT * FROM poblacion_brasil", engine)

df = poblacion_brasil.merge(states, how='inner', on='id_state')
df_2010 = df[(df['anio'] >= 2010)] # La tabla contenía otros años, sin embargo solo se tomó en cuenta el último registro oficial en 2010 a nivel estatal

df_2010['n_0_14']= (df['prop_0_14'] * df['poblacion_total'])/100 # Se crearon nuevas variables para convertir las proporciones en valores absolutos
df_2010['n_15_64']= (df['prop_15_64'] * df['poblacion_total'])/100 
df_2010['n_65_up']= (df['prop_65_up'] * df['poblacion_total'])/100 
df_2010['n_15_59']= (df['prop_15_59'] * df['poblacion_total'])/100 
df_2010['n_60_up']= (df['prop_60_up'] * df['poblacion_total'])/100 

df2 = df_2010.groupby(['id_region']).sum() # Se agruparon los datos de población por región y se eligieron las variables de interés
df2 = df2.merge(regions, how='inner', on='id_region')
df3 = df2[['id_region','name_region','poblacion_total','poblacion_hombres','poblacion_mujeres','nacimientos','n_0_14','n_15_64','n_65_up','n_15_59','n_60_up']]
df3['prop_0_14'] = (df3['n_0_14'] / df3['poblacion_total']) * 100 # ya agrupado por región se convirtió de nuevo a proporciones los valores por grupo de edad
df3['prop_15_64'] = (df3['n_15_64'] / df3['poblacion_total']) * 100
df3['prop_65_up'] = (df3['n_65_up'] / df3['poblacion_total']) * 100
df3['prop_15_59'] = (df3['n_15_59'] / df3['poblacion_total']) * 100
df3['prop_60_up'] = (df3['n_60_up'] / df3['poblacion_total']) * 100

df4 = df3[['id_region','name_region','poblacion_total','poblacion_hombres','poblacion_mujeres','nacimientos','prop_0_14','prop_15_64','prop_65_up','prop_15_59','prop_60_up']]
    
#-----------------------------------------------------------------------#   

D, E, F = st.columns(3)

with D:
    st.markdown("Analisis de la poblacion de Brasil")


E.image(Image.open("Streamlit/Images/regiones.png"))


with F:
    st.write(df4)


G = st.columns(1)

#--------------------------------------------------------------------#

df5 = df4[['name_region', 'prop_0_14', 'prop_15_64', 'prop_65_up']]

df5.plot(
    x = 'name_region',
    kind = 'bar',
    stacked = True,
    mark_right = True,
    color= ('silver','gray','black'),
    figsize=(6,4),
    fontsize= 15
    )

plt.xticks(rotation=45, fontsize=8)
plt.ylabel("Percentage", fontsize=16)
plt.xlabel("Region", fontsize=16)
plt.legend(('0 a 14 years', '15 a 64 years', 'up to 65 years'), bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.title('Percentage distribution of population \n in Brazil by Regions (2010)', fontsize=20, y=1.1)
a = plt.show()

with G:
    G.markdown("Grafica de poblacion")
    st.write(a)

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

elif option == "Average amount of money spent per states": 

    st.header("Media de dinero gastado por estado") 
    HtmlFile = open("Streamlit/Geoespatial-Drafts/payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

else:
    st.header("PIB Percapita)")
    HtmlFile = open("Streamlit/Geoespatial-Drafts/percapitamap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)


