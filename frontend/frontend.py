import streamlit as st
from  datetime import datetime
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


st.markdown("""
    # Welcome to the Olympics App

    ## Where you can find usefull **information** and **results** from *1806* till *2022*

""")

col1, col2, col3, col4 = st.columns(4)

option = col1.selectbox('Select edition', ['Olympics', 'Summer', 'Winter', 'Intercalated'])

initial_year = col2.selectbox('Initial year', range(1896,2023))
final_year = col3.selectbox('Final year', range(1896,2023))

number_countries = col4.text_input('Number of countries', '20')

buton = st.button('Analyse')
url = 'http://127.0.0.1:8000/best_countries'
if buton :
    params = {'desired_edition': option,
              'initial_year': initial_year,
              'final_year': final_year,
              'number_countries': number_countries}

    response = requests.get(url, params=params).json()

    x = response['countries']
    width = 0.5  # the width of the bars
    figu = plt.figure(figsize=(50,30))
    ax = plt.subplot()


    ax.bar(x , list(response['gold']), width, align='center', label ='Gold')
    ax.bar(x , list(response['silver']), width, align='center', label ='Silver')
    ax.bar(x , list(response['bronze']), width, align='center', label ='Bronze')
    plt.legend(prop={'size': 60})
    plt.rcParams.update({'font.size': 45})
    plt.title(f'Medals for the {number_countries} first countrys')
    plt.xlabel('Countries')
    plt.ylabel('Total number of medals ')
    st.pyplot(figu)

    # Posible mejore , crear un grafico iterativo
