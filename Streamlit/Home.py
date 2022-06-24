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

A1.image(Image.open())

with B:
    st.markdown('''# Platzi Master Cohort 10
    Bussines Intelligence Team
    - Julián Castro     - Ricardo Escamilla
    - Emmanuel Escobar  - Marco Rocha
    - Juan Rincon       - Robert Barrios
    ''')

with C:
    st.text("MIMIM")


