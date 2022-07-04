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
    st.markdown("# Platzi Master Cohort 10")
    st.markdown("## Bussines Intelligence Team")

    st.markdown('''
    - [Julián Castro](Julian.com)     - Ricardo Escamilla
    - Emmanuel Escobar  - Marco Rocha
    - Juan Rincon       - Robert Barrios''')


with A:
    st.title("Bussines Intelligence")
    st.markdown("### Tomar desiciones inteligentes basadas en datos")
    st.markdown("Durante cuatro meses el equipo de BI aprendió a **sacarle provecho a los datos** mediante diversas herramientas y tecnologias de analisis **para potenciar tu negocio**")
    st.markdown("Este trabajo recoge las conclusiones para **OLIST, un comercio electronico de Brasil con más de 100000 registros entre el 2016 y el 2018**")

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


D.image(Image.open("Streamlit/Images/Poblacion.png"))

E.image(Image.open("Streamlit/Images/regiones.png"))


with F:
    st.write(df4)

#---------------------------------------------------------#

I, J, K = st.columns(3)

#Clientes con las ordenes

clients_total = pd.merge(customers, orders, on='customer_id')
orders_total = pd.merge(orders_payments, orders_reviews, on='order_id')
df_clients = pd.merge(clients_total, orders_total, on='order_id')

#Vendedores con los productos

sellers_total = pd.merge(sellers, order_items, on='seller_id')
products_total = pd.merge(products, category_name_translation, on='product_category_name')
df_products = pd.merge(sellers_total, products_total, on='product_id')
df = pd.merge(df_clients, df_products, on='order_id')

dt=df.select_dtypes(include='object').fillna('None')
df_clean = df.fillna(dt)

with I:
    dict = {'index': 'customer_state','customer_state': 'Count'}
    total_customer_state = pd.DataFrame(df_clean['customer_state'].value_counts().reset_index().rename(columns=dict).sort_values(by=['Count'],ascending=False))

    fig = plt.figure(figsize =([12, 12])) 
    sns.set_style('darkgrid')
    plt.style.use('ggplot')
    g = sns.barplot(x=total_customer_state['customer_state'], y=total_customer_state['Count'], palette='Greens_r', orient="v")
    plt.title('Distribución de consumidores por Estado', size=36, y=1.03)
    plt.yticks(fontsize=18, color='gray');
    plt.ylabel('Número de clientes', fontsize=24)
    plt.xlabel('Estados', fontsize=24)
    plt.xticks(fontsize=18, rotation=45)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)

    st.write(fig)


with J:
    st.markdown("Brasil es uno de los paises más grandes del mundo, abarca el 45% del america del sur, en su extensión viven más de 200 millones de habitantes; debido a la gran extensión del pais se divide en cinco regiones.")
    st.markdown("Cuenta con 25 habitantes por Km2, siendo uno de los paises menos densamente poblados.")
    st.markdown("*Usando datos externos* pudimos ver que **la region sur y sureste son la que mayor ingreso por persona tienen**. Haciendose evidente la desigualdad del pais, donde el **10% de sus habitantes tiene el 50% del producto nacional**")
    
    st.markdown("Especialmente, El movimientos del comercio está concentrado en 6 estados. **¿Que hace especiales a nivel demografico estos estados?**")

with K:

    total_payment_value = pd.DataFrame(df_clean.groupby(by=["customer_state"])["payment_value"].sum().reset_index().sort_values(by=['payment_value'],ascending=False))
    
    fig = plt.figure(figsize =([14, 14])) 
    sns.set_style('darkgrid')
    plt.style.use('ggplot')
    g = sns.barplot(x=total_payment_value['customer_state'], y=total_payment_value['payment_value'], palette='Greens_r', orient="v")
    plt.title('Total de dinero Facturado por Estado', size=36, y=1.03)
    plt.yticks(fontsize=18, color='gray');
    plt.ylabel('Dinero Facturado', fontsize=24)
    plt.ticklabel_format(style='plain', axis='y')
    plt.xlabel('Estado', fontsize=24)
    plt.xticks(fontsize=18, rotation=45)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)

    st.write(fig)

#--------------------------------------------------------------------------------------#    

st.header("Visualizaciones demograficas por estado")
st.markdown("Elegimos tres variables que afectan directamente a las compras del comercio electronico, puedes verlas en el mapa desplegable")

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) 

option = st.selectbox(
     'Seleccionar variable',
     ('Compras por estado', 'Media de dinero gastada', 'Ingreso por persona'))

if option == "Compras por estado":

    st.header("Número de compras por estado")
    HtmlFile = open("Streamlit/Geoespatial-Drafts/count.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

elif option == "Media de dinero gastada": 

    st.header("Media de dinero gastado por estado") 
    HtmlFile = open("Streamlit/Geoespatial-Drafts/payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

else:
    st.header("Ingreso por persona)")
    HtmlFile = open("Streamlit/Geoespatial-Drafts/percapitamap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)


#-------------------------------------------------------#

L,M = st.columns(2)


L.image(Image.open("Streamlit/Images/Payments.png"))


with M:
    st.markdown("Tras analizar estas graficas, podemos ver que hay una gran influencia en las compras realizadas debido a la cantidad de dinero que tienen los brasileños")
    st.markdown("Sumado a eso, la concentración de dinero en las regiones del sur se ve reflejado en los pedidos realizados y el retraso en las entregas.")

    st.markdown("Si hacemos un analisis de los medios del pago, podemos ver que estas dos regiones son las que tienen mayor acceso a estos, de acuerdo al banco de brasil, el 86% de los ciudadanos tienen acceso a un telefono, pero el 56% tienen acceso a un medio de pago")
#------------------------------------------------------#

st.markdown("***")

#--------------------------------------------------------#

st.markdown("### Ley de Pareto")

S,T = st.columns(2)

S.image(Image.open("Streamlit/Images/Pareto.jpg"))

with T:
    st.markdown("Hay un gran mercado en Brasil para los comercios electronicos, en dos años, OLIST registró 112650 ordenes, siendo salud y belleza la categorias más comprada de productos")

    st.markdown("En estos dos años se registraron 3053 vendedores")

    st.markdown("De acuerdo a Pareto, el 80% de los resultados son producidos por el 20% de las acciones. Y OLIST no deja de cunplir esta ley. ")
    st.markdown("El 80% de las ventas (86680) fueron realizados por 535 vendedores. ")


#-------------------------------------------------------
st.markdown("***")
#------------------------------------------------------#

st.markdown("### Sobre las calificaciones")

N,O = st.columns(2)

N.image(Image.open("Streamlit/Images/UnidadesVendidas.png"))
O.image(Image.open("Streamlit/Images/ScorePromedio.png"))



Q, R = st.columns(2)

Q.image(Image.open("Streamlit/Images/Puntuaciones.png"))

with R:
    st.markdown("Encontramos que el numero de unidades vendidas no tiene influencia directa sobre las calificaciones realizadas por los usuarios.")
    st.markdown("Se evidencia que las calificaciones son en su mayoria positivas; y si bien, nuestro analaisis no se enfocó en un analisis de entregas; pero se muestra que la mayoria de calificaciones negativas se debe a las entregas retrasadas")
    st.markdown("Le recomendamos a OLIST cambiar sus sistema de puntuación en una escala de tres opiniones")

#-------------------------------------------------------------------#

st.markdown("***")

#-------------------------------------------------------------------#

st.markdown("A priori Algorithm")

P, U, V = st.columns(3)

P.image(Image.open("Streamlit/Images/Top10.png"))
U.image(Image.open("Streamlit/Images/Apriori.png"))

with V:
    V.markdown("Viendo el top 10 productos más comprados (donde se concentran la mayoria de las compras del comercio electronico) queremos saber si hay alguna tendencia de compras")
    st.markdown("**En este [analisis](https://share.streamlit.io/felipesalda/brazilian-e-commerce/main/dashboard.py) se puede ver que el 97% de usuarios hace solo una compra en OLIST**")
    st.markdown("Para usar reglas de asociacion deberiamos tener más datos que pueden relacionarse en una sola compra, pero con el 3% nos damos cuenta que hay un patron de compras")

#---------------------------------------------------------------------#

