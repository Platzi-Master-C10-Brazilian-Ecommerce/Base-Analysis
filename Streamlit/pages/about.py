#Librerias usadas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#dashboard
import streamlit as st
import plost
from PIL import Image



# Configuración de la pagina
st.set_page_config(page_title="Bussines Intelligence Team",page_icon="🪙",layout="wide")


a1, a2 = st.columns(2)
a1.image(Image.open('Streamlit\pages\Media_Resources\PM_LOGO.jpg'))
with a2:
    st.markdown('''# Platzi Master Cohort 10
    Bussines Intelligence Team
    - Julián Castro     - Ricardo Escamilla
    - Emmanuel Escobar  - Marco Rocha
    ''')
    a2.metric("2017-2018 Growth",format(products_Maximun["%Growth"].iloc[0],'.2f')+'%')
