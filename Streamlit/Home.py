#Librerias usadas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
from PIL import Image


# Configuración de la pagina
st.set_page_config(page_title="Bussines Intelligence Team",page_icon="📈",layout="wide")


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

st.header("A priori")

with J:
    pass

#---------------------------------------------------------#

M, O = st.columns(2)

st.header("Maps")

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) # Javascrip object notation 

option = st.selectbox(
     'Display query',
     ('Count products', 'Payments products', 'percapita'))

if option =="Count products":
    st.header("")
    HtmlFile = open("Data-Analysis-for-Brazilian-E-commerce/Data-Analysis-Drafts/Emmanuel HTML/count.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)
elif option =="Payments products":  
    st.header("") 
    HtmlFile = open("Data-Analysis-for-Brazilian-E-commerce/Data-Analysis-Drafts/Emmanuel HTML/payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)
else:
    st.header("")
    HtmlFile = open("Data-Analysis-for-Brazilian-E-commerce/Data-Analysis-Drafts/Emmanuel HTML/payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)


