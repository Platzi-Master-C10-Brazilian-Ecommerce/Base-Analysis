import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://usuario_consulta:platzicohort10@platzicohort10.cig2rbjhhqmz.us-east-1.rds.amazonaws.com/Brazilian_e_commerce')

with engine.connect() as con:
  rs = con.execute("SELECT product_id,price FROM olist_order_items_dataset WHERE price > 6000") # query que vamos a realizar
  df = pd.DataFrame(rs.fetchall()) # lectura de las filas, hay mas opciones
  df.columns = rs.keys()


df = df.sort_values(by=['price'], ascending=True)
# Plot the fur data using Seaborn's countplot
fig, ax = plt.subplots(figsize=(10, 5))
sns.set_style("dark")
ax = sns.histplot(data=df, x='price', y='product_id', hue='product_id')


st.title('Datos de AWS, tabla olist_order_items_dataset')
st.text('consulta product_id con los precios mayores a 5000')
st.dataframe(data=df)
st.pyplot(fig)