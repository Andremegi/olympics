import streamlit as st
import os
import pandas as pd
import requests

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to documents
path_to_docs = os.path.join(path, '..','..','olympics_folder','documents')
country_profiles_df = pd.read_csv(f'{path_to_docs}/Olympic_Country_Profiles.csv', skipinitialspace=True)
countries= country_profiles_df['noc'].unique()

st.markdown("""
            ## In this page you can dig into a country evolution year per year
            """)


country = st.selectbox('Select sport', countries)
url ='http://127.0.0.1:8000/country_evolution'
params = {'country_noc':country}



response = requests.get(url, params=params).json()
country_ev_df = pd.DataFrame(response[0])
table_country_ev_df = pd.DataFrame(response[1])
st.markdown(f"the evolution for {country_ev_df.loc[0]['country']} :")
st.line_chart(country_ev_df, x='year', y='total', color='edition')

st.table(table_country_ev_df)

st.markdown('## Would you like to dig deeper into the information?')
year = st.selectbox('Select a year', range(1896,2023))
buton = st.button('Select')
if buton:
    url3= 'http://127.0.0.1:8000/deeper_country_evolution'
    params3= {'year':year,
            'country_noc':country}
    response3 = requests.get(url3,params=params3).json()

    year_info_df = pd.DataFrame(response3)
    st.table(year_info_df)
else:
    st.markdown('Select a year and find the info')
