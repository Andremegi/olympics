import streamlit as st
from  datetime import datetime
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


st.markdown("""
    ## Here you can compare the number of medals each country won according to :
    - Different editions of the Olympics:
        - summer ('Summer')
        - winter ('Winter')
        - both ('Olympics')
        - special edition held in 1906 ('Intercalated').
    - For as many years as you wish between 1896 and 2022
    - As many countries as you wish (number of countries)


""")

col1, col2, col3, col4 = st.columns(4)

option = col1.selectbox('Select edition', ['Olympics', 'Summer', 'Winter', 'Intercalated'])

initial_year = col2.selectbox('Initial year', range(1896,2023))
final_year = col3.selectbox('Final year', range(1896,2023))

number_countries = col4.text_input('Number of countries', '20')

buton = st.button('Analyse')
url = 'http://127.0.0.1:8000/best_countries?'
if buton :
    params = {'desired_edition': option,
              'initial_year': initial_year,
              'final_year': final_year,
              'number_countries': number_countries}

    response = requests.get(url, params=params).json()

    colors = ['#B8860B', '#FFD700',  '#A9A9A9']

    #Create dataframe to be able to plot with st(with more info) and then create comparative tables
    df = pd.DataFrame.from_dict(response)
    sorted = df.sort_values('total', ascending = False)
    sorted_non_spaces = sorted.copy()
    i=0
    for l,country in sorted[['best_countries']].iterrows():
        sorted.loc[i,'best_countries'] = f'{country[0].rjust(int(number_countries)+1 - i)}'
        i += 1

    df = sorted.set_index('best_countries')
    df =df[['gold','silver','bronze']]
    st.markdown(f'In the next chart it is represented the gold, silver and bronze medals from the best **{number_countries}** countires in **descending** order')
    st.markdown("""### MEDALS PER COUNTRY""")
    st.bar_chart(df, color = colors)

    sorted_non_spaces['medal/athletes best countries'] = response['proport_countries']

    st.markdown(f'Bellow we compare the first **{number_countries}** countries in **descending** order, regarding:')
    st.markdown("""
                - On the first column *best_countries* we represent the best countries having in count their medals
                - On the second columns *medal/athletes best countries* we calculate a proportion of the number of medals and the number of athlets
                """)
    st.table(sorted_non_spaces[['best_countries','medal/athletes best countries']])


    # Posible mejore , crear un grafico iterativo
