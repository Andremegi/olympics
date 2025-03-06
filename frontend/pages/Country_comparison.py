import streamlit as st
from  datetime import datetime
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from olympics_folder.simple_analyzer import country_con_noc


st.markdown("""
    ### Here you can compare the number of medals each country won according to :
    - Different editions of the Olympics:
        - Summer ('**Summer**')
        - Winter ('**Winter**')
        - Both ('**Olympics**')
        - Special edition held in 1906 ('**Intercalated**').
        - Special edition held in 1956 ('**Equestrian**')
    - The years that you wish between 1896 and 2022 ('**Initial year**' and '**Final year**')
    - The number of countries  you want ('**Number of countries**')


""")

col1, col2, col3, col4 = st.columns(4)

option = col1.selectbox('Select edition', ['Olympics', 'Summer', 'Winter', 'Intercalated', 'Equestrian'])

initial_year = col2.selectbox('Initial year', range(1896,2023))
final_year = col3.selectbox('Final year', range(1896,2023))

number_countries = col4.text_input('Number of countries', '20')

# Case intercalated so it shows automatically what needs to be shown
if option =='Intercalated':
    initial_year = 1906
    final_year = 1906
    st.markdown(f'**Intercalted** is a special edition cariied out in **1906** where only 17 countries compited')

if option =='Equestrian':
    initial_year = 1956
    final_year = 1956
    st.markdown(f'**Intercalted** is a special edition cariied out in **1956** where only 7 countries compited ')

buton = st.button('Analyse')
url = 'http://127.0.0.1:8000/best_countries?'
if buton :
    params = {'desired_edition': option,
              'initial_year': initial_year,
              'final_year': final_year,
              'number_countries': number_countries}

    response = requests.get(url, params=params).json()

    colors = ['#FFD700', '#C0C0C0',  '#B8860B']

    #Create dataframe to be able to plot with st(with more info) and then create comparative tables
    df = pd.DataFrame.from_dict(response)
    sorted = df.sort_values('total', ascending = False)
    sorted_non_spaces = sorted.copy()
    i=0
    for l,country in sorted[['best_countries']].iterrows():
        sorted.loc[i,'best_countries'] = f'{country[0].rjust(int(number_countries)+10 - i)}'
        i += 1

    df = sorted.set_index('best_countries')
    df =df[['gold','silver','bronze']]
    df.columns = ['1.Gold', '2.Silver', '3.Bronze']

    st.markdown(f'In the next chart it is represented the gold, silver and bronze medals from the best **{number_countries}** countires in **descending** order')
    st.markdown("""### MEDALS PER COUNTRY""")

    st.bar_chart(df, color = colors)

    sorted_non_spaces['medal/athletes best countries'] = response['proport_countries']
    sorted_non_spaces['medal/athletes best countries country '] = sorted_non_spaces['medal/athletes best countries'].apply(lambda row : country_con_noc(row))
    sorted_non_spaces['best countries country'] = sorted_non_spaces['best_countries'].apply(lambda row : country_con_noc(row))

    st.markdown(f'Bellow we compare the first **{number_countries}** countries in **descending** order, regarding:')
    st.markdown("""
                - The first column *best_countries country* represents the best countries having regarding their medals
                - The second column *medal/athletes best countries country*  represents a ratio between the number of medals and the number of athlets eaxh country has in descending order

                """)
    st.table(sorted_non_spaces[['best countries country','medal/athletes best countries country ' ]])
