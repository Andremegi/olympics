import streamlit as st
from  datetime import datetime
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import os



# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to documents
path_to_docs = os.path.join(path, '..','..','olympics_folder','documents')
athlete_event_detailed_df = pd.read_csv(f'{path_to_docs}/Olympic_Athlete_Event_Details.csv', skipinitialspace=True)
sports= athlete_event_detailed_df['sport'].unique()

cola, colb = st.columns(2)
sport = cola.selectbox('Select sport', sports)
ath = athlete_event_detailed_df[athlete_event_detailed_df['sport']==sport]['athlete'].unique()
athlete = colb.selectbox('Select athlete', ath)

url ='http://127.0.0.1:8000/athlete_evolution?'
params ={'sport':sport,
         'name': athlete}

response = requests.get(url, params=params).json()



st.markdown('# General information:')
col1, col2, col3 = st.columns(3)
col1.metric("", "Country", response['country'][0])
col2.metric("", "Sex", response['sex'][0])
col3.metric("", "Born", response['born'][0])

col1_2, col2_2 = st.columns(2)
col1.metric("", "Weight", response['weight'][0])
col2.metric("", "Heigth", response['height'][0])

st.markdown(f"- **Description** : {response['description'][0]}")
st.markdown(f"- **Special notes** : {response['special notes'][0]}")

st.markdown('- Olympic year and age the athlete where when compited: ')

athlete_needed =pd.DataFrame.from_dict(response)
year_table = athlete_needed[['Edition','Age']].drop_duplicates().set_index('Edition')
st.table(data=year_table )
athlete_evolution = athlete_needed.groupby('Edition', as_index=False)[['Edition','Medal']].value_counts()
athlete_evolution = athlete_evolution.rename(columns={'count': 'Number of medals'})

athlete_evolution.loc[athlete_evolution['Medal']==0 ,'Number of medals'] = 0
edition_medals = athlete_evolution.groupby('Edition', as_index=False)[['Edition','Number of medals']].sum()
edition_medals['Edition'] = edition_medals['Edition'].apply(lambda row : row[0:4])

st.markdown('# Evolution of medals in the different olympics edition')
st.line_chart(data = edition_medals, x='Edition' ,y ='Number of medals',  x_label ='Olympic year', y_label ='Number of medals')

athlete_evolution.loc[athlete_evolution['Medal'] == 0 ,'Medal'] = 'No medals'
athlete_evolution.loc[athlete_evolution['Medal'] == 'No medals' ,'Number of medals'] = 1
st.markdown(" Deep depiction of the medals ")
st.table(athlete_evolution.set_index('Edition'))
