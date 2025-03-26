import streamlit as st
import os
import pandas as pd
import requests

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to documents
path_to_docs = os.path.join(path, '..','..','olympics_folder','documents')
country_profiles_df = pd.read_csv(f'{path_to_docs}/Olympic_Country_Profiles.csv', skipinitialspace=True)
countries= country_profiles_df['country'].unique()

st.markdown("""
            ### On this page you can learn more about the evolution of each country year by year
            """)


country = st.selectbox('Select country', countries)
url_render ='https://olympiastats.onrender.com/country_evolution?'
#localurl: url ='http://127.0.0.1:8000/country_evolution'

#localurl: url_country_name ='http://127.0.0.1:8000/country_to_noc?'
url_country_name_render ='https://olympiastats.onrender.com/country_to_noc?'
param = requests.get(url_country_name_render, params = {'argument':country}).json()['name']
params = {'country_noc': param }



response = requests.get(url_render, params=params).json()
country_ev_df = pd.DataFrame(response[0])
table_country_ev_df = pd.DataFrame(response[1]).sort_values('year', ascending = True)
table_country_ev_df.rename(columns={'year':'Year',
                                    'edition': 'Edition',
                                    'total':'Total medals',
                                    'gold':'Gold medals',
                                    'silver':'Silver medals',
                                    'bronze':'Bronze medals',
                                    'num_ath':'Athlets'}, inplace = True)
table_country_ev_df = table_country_ev_df.set_index('Year')
if country_ev_df.empty:
    st.markdown('Ups it seems that this country has no medals yet')
else:
    st.markdown(f"The evolution for {country_ev_df.loc[0]['country']} :")
    st.line_chart(country_ev_df, x='year', y='total', color='edition', y_label= 'Total number of medals', x_label='Year')
    st.table(table_country_ev_df)


st.markdown('### Would you like to dig deeper into the information on any specific year?')
year = st.selectbox('Select a year', range(1896,2023))
buton = st.button('Select')
if buton:
    url3_render = 'https://olympiastats.onrender.com/deeper_country_evolution?'
    #local url : url3= 'http://127.0.0.1:8000/deeper_country_evolution'
    params3= {'year':int(year),
            'country_noc': param}
    response3 = requests.get(url3_render,params=params3).json()

    year_info_df = pd.DataFrame(response3)
    st.table(year_info_df)
else:
    st.markdown('Select a year and find the info')
