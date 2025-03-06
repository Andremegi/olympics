import streamlit as st
import os
import pandas as pd
import requests
from olympics_folder.simple_analyzer import country_to_noc

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to documents
path_to_docs = os.path.join(path, '..','..','olympics_folder','documents')
country_profiles_df = pd.read_csv(f'{path_to_docs}/Olympic_Country_Profiles.csv', skipinitialspace=True)
countries= country_profiles_df['country'].unique()

st.markdown("""
            ### On this page you can learn more about the evolution of each country year by year
            """)


country = st.selectbox('Select sport', countries)
url ='http://127.0.0.1:8000/country_evolution'
params = {'country_noc': country_to_noc(country)}



response = requests.get(url, params=params).json()
country_ev_df = pd.DataFrame(response[0])
table_country_ev_df = pd.DataFrame(response[1])

if country_ev_df.empty:
    st.markdown('Ups it seems that this country has no medals jet')
else:
    st.markdown(f"the evolution for {country_ev_df.loc[0]['country']} :")
    st.line_chart(country_ev_df, x='year', y='total', color='edition')
    st.table(table_country_ev_df)


st.markdown('### Would you like to dig deeper into the information on any specific year?')
year = st.selectbox('Select a year', range(1896,2023))
buton = st.button('Select')
if buton:
    url3= 'http://127.0.0.1:8000/deeper_country_evolution'
    params3= {'year':int(year),
            'country_noc':country_to_noc(country)}
    response3 = requests.get(url3,params=params3).json()

    year_info_df = pd.DataFrame(response3)
    st.table(year_info_df)
else:
    st.markdown('Select a year and find the info')
