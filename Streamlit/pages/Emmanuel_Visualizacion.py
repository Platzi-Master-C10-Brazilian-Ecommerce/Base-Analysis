from Visualizations import Data_Viz_Emmanuel_Test as EVs



import streamlit as st
#Todo lo que tenga el (st) es obra de stramlit


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from sqlalchemy import create_engine
from PIL import Image


#Se borró el codigo de la visuzliacion y será llamado desde


st.text('Count of sales by year')
code = '''dfplot = df_ord.groupby(df_ord['order_purchase_timestamp'].dt.year).count()'''  #(1)
#el code es para poner una linea de texto con el codigo
st.code(code, language='python')

#Cada dfplot es lo que nosotros deberiamos llamar

dfplot , fig = EVs.plot1()
st.dataframe(data=dfplot)
st.pyplot(fig)

# st.text('Count of sales by day')
# st.dataframe(data=dfplot2)
# st.pyplot(fig2)

# st.text('Mean of sales by day')
# st.dataframe(data=dfplot3)
# st.pyplot(fig3)

# st.text('Median of sales by day')
# st.dataframe(data=dfplot4)
# st.pyplot(fig4)