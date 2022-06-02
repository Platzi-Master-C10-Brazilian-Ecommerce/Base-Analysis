import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from sqlalchemy import create_engine
from PIL import Image


#Se establece la conexión con la basse de datos remota
host1 = 'platzicohort10@platzicohort10.cig2rbjhhqmz.us-east-1.rds.amazonaws.com'
user1 = 'usuario_consulta'
password1 = 'platzicohort10'
database1 = 'Brazilian_e_commerce'

engine = create_engine('postgresql+psycopg2://'+
                       user1+':'+
                       host1+'/'+
                       database1)

def query_psql(consulta):
    with engine.connect() as con:
      rs = con.execute(consulta)
      cols = rs.keys()
      row = rs.fetchall()
      df = pd.DataFrame(row)
      df.columns = cols
    return df

with engine.connect() as con:
    rs = con.execute("""SELECT * FROM pg_catalog.pg_tables 
                      WHERE schemaname != 'pg_catalog' 
                      AND schemaname != 'information_schema'""")
    row = rs.fetchall()
    df_tables = pd.DataFrame(row)
    #print(f'Tablas de la base de datos:\n {df_tables[1]}')

with engine.connect() as con:
  rs = con.execute("SELECT product_id,price FROM olist_order_items_dataset WHERE price > 6000") # query que vamos a realizar
  df = pd.DataFrame(rs.fetchall()) # lectura de las filas, hay mas opciones
  df.columns = rs.keys()

sql1 = "SELECT * FROM olist_orders_dataset"
orders = query_psql(sql1)
orders.order_purchase_timestamp = orders.order_purchase_timestamp.astype('datetime64[ns]')
sql2 = "SELECT * FROM olist_order_items_dataset"
order_items = query_psql(sql2)

#Juntar dataframes
df_order = pd.merge(left = order_items, right = orders,
                   how = "inner",
                   left_on = ["order_id"],
                   right_on = ["order_id"])

df_ord = df_order.sort_values(by='order_purchase_timestamp') 
df_ord.index = df_ord.order_purchase_timestamp
dfplot = df_ord.groupby(df_ord['order_purchase_timestamp'].dt.year).count()
dfplot.plot(figsize=(30,15))
fig, ax = plt.subplots(figsize=(10, 5))
sns.set_style("dark")
ax = sns.lineplot(data=dfplot)

dfplot2 = df_ord.resample('D').count()
dfplot2.plot(figsize=(30,15))
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.set_style("dark")
ax2 = sns.lineplot(data=dfplot2)

dfplot3 = df_ord.resample('D').mean()
dfplot3.plot(figsize=(30,15))
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.set_style("dark")
ax3 = sns.lineplot(data=dfplot3)

dfplot4 = df_ord.resample('D').median()
dfplot4.plot(figsize=(30,15))
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.set_style("dark")
ax4 = sns.lineplot(data=dfplot4)

st.title('Brazilian e-comerce cohort 10')
image = Image.open('activitylist.png')
st.image(image)

st.write("[Notion of the activities](https://www.notion.so/3250b16f6a7b47eab7644abbe65fd9ac?v=33d926d3d43b46c6b4abe028a2d42e1f)")


st.text('Count of sales by year')
code = '''dfplot = df_ord.groupby(df_ord['order_purchase_timestamp'].dt.year).count()'''
st.code(code, language='python')
st.dataframe(data=dfplot)
st.pyplot(fig)

st.text('Count of sales by day')
st.dataframe(data=dfplot2)
st.pyplot(fig2)

st.text('Mean of sales by day')
st.dataframe(data=dfplot3)
st.pyplot(fig3)

st.text('Median of sales by day')
st.dataframe(data=dfplot4)
st.pyplot(fig4)