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
            ### Learn more about the evolution of the medals of each country year by year
            """)


country = st.selectbox('Select country', countries)

url_render ='https://olympiastats.onrender.com/country_evolution?'
#url ='http://127.0.0.1:8000/country_evolution'

#url_country_name ='http://127.0.0.1:8000/country_to_noc?'
url_country_name_render ='https://olympiastats.onrender.com/country_to_noc?'
param = requests.get(url_country_name_render, params = {'argument':country}).json()['name']
params = {'country_noc': param }



response = requests.get(url_render, params=params)
#response.raise_for_status()  # raises exception when not a 2xx response
if str(response.status_code)[0] in '45':
        st.markdown(f'# Error {response.status_code}, please reload the window')
if response.status_code != 204:
    response = response.json()
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
        country_ev_df['year'] = country_ev_df['year'].astype(str)
        st.markdown(f"The evolution for {country_ev_df.loc[0]['country']} :")
        st.line_chart(country_ev_df, x='year', y='total', color='edition', y_label= 'Total number of medals', x_label='Year')
        st.table(table_country_ev_df)

        st.markdown('### Would you like to dig deeper into the information from any specific year?')

        year = st.selectbox('Select a year', table_country_ev_df.index)
        buton2 = st.button('Select')
        if buton2:
            url3_render = 'https://olympiastats.onrender.com/deeper_country_evolution?'
            #url3= 'http://127.0.0.1:8000/deeper_country_evolution'
            params3= {'year':int(year),
                    'country_noc': param}
            response3 = requests.get(url3_render,params=params3)
            #response3.raise_for_status()  # raises exception when not a 2xx response
            if str(response3.status_code)[0] in '45':
                st.markdown(f'# Error {response.status_code}, please reload the window')
            if response3.status_code != 204:
                response3 = response3.json()
                year_info_df = pd.DataFrame(response3)
                year_info_df = year_info_df.set_index('sport')
                year_info_df = year_info_df.rename(columns={'sport':'Sport','number_medals':'Number of medals'})
                st.table(year_info_df)
        else:
            st.markdown('Select a year and find the info')
