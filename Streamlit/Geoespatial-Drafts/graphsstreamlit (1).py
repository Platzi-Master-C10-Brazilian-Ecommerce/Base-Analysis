import streamlit as st
import streamlit.components.v1 as components
import json
from urllib.request import urlopen

#Importing Brazil’s geographic information
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) # Javascrip object notation 

option = st.selectbox(
     'Display query',
     ('Count products', 'Payments products', 'percapita'))

if option =="Count products":
    st.header("")
    HtmlFile = open("count.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)
elif option =="Payments products":  
    st.header("") 
    HtmlFile = open("payment.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)
else:
    st.header("")
    HtmlFile = open("percapitamap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)
