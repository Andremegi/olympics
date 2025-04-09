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

st.markdown('### Search for information about athletes of your interest')
cola, colb = st.columns(2)
sport = cola.selectbox('Select sport', sports)
ath = athlete_event_detailed_df[athlete_event_detailed_df['sport']==sport]['athlete'].unique()
athlete = colb.selectbox('Select athlete', ath)

buton = st.button('Search')
if buton:
    #url ='http://127.0.0.1:8000/athlete_evolution?'
    #url_render = 'https://olympiastats.onrender.com/athlete_evolution?'
    url_railways = 'https://olympics-production-247f.up.railway.app/athlete_evolution?'
    params ={'sport':sport,
            'name': athlete}

    response = requests.get(url_railways, params=params)
    if response.status_code >= 400:
        try:
            data = response.json()
            st.error(f"Error {response.status_code}: {data}")
            st.error('### Please reload the window ')
            st.stop()
        except Exception as e:
            st.error(f"Error {response.status_code}: Could not parse backend response.")
            st.write("Raw response:")
            st.code(response.text)
        st.stop()
    if response.status_code != 204:
        response = response.json()

        response['isTeamSport'] = list(map(lambda x: 'Yes' if x == True else '-No', response['isTeamSport']))
        st.markdown('# General information:')
        col1, col2, col3 = st.columns(3)
        col1.metric("", "Country", response['country'][0])
        col2.metric("", "Sex", response['sex'][0])
        col3.metric("", "Born", response['born'][0])

        col1_2, col2_2 = st.columns(2)
        col1.metric("", "Weight", response['weight'][0])
        col2.metric("", "Heigth", response['height'][0])
        col3.metric("",'Is team sport?', response['isTeamSport'][0])

        st.markdown(f"- **Description** : {response['description'][0]}")
        st.markdown(f"- **Special notes** : {response['special notes'][0]}")

        st.markdown('- Olympic year and age the athlete where when compited: ')

        athlete_needed =pd.DataFrame.from_dict(response)
        year_table = athlete_needed[['Edition','Age']].drop_duplicates().set_index('Edition')
        year_table['Age'] = year_table['Age'].astype(int)
        st.table(data=year_table )
        athlete_evolution_table = athlete_needed.groupby('Edition', as_index=False)[['Edition','event','Medal','position']].value_counts()
        athlete_evolution_table = athlete_evolution_table.rename(columns={'count': 'Number of medals', 'event': 'Event'})
        athlete_evolution_table.loc[athlete_evolution_table['Medal'] == 0 ,'Medal'] = 'No medals'
        athlete_evolution_table.loc[athlete_evolution_table['Medal'] == 'No medals' ,'Number of medals'] = 0

        athlete_evolution = athlete_needed.groupby('Edition', as_index=False)[['Edition','Medal']].value_counts()
        athlete_evolution = athlete_evolution.rename(columns={'count': 'Number of medals'})
        athlete_evolution.loc[athlete_evolution['Medal']==0 ,'Number of medals'] = 0

        edition_medals = athlete_evolution.groupby('Edition', as_index=False)[['Edition','Number of medals']].sum()
        edition_medals['Edition'] = edition_medals['Edition'].apply(lambda row : row[0:4])

        st.markdown('# Evolution of medals in the different olympics edition')
        st.line_chart(data = edition_medals, x='Edition' ,y ='Number of medals',  x_label ='Olympic year', y_label ='Number of medals')


        st.markdown(" Deep depiction of the medals ")
        st.table(athlete_evolution_table.set_index('Edition'))
        df_acron = pd.DataFrame({
    'Acronym': ['AC', 'DNF', 'DNQ', 'DNS', 'DQ', 'EL', 'HC', 'HM', 'MNK', 'NH', 'NM', 'NP', 'NVL', 'TNK', 'EL']
})

        # Diccionario de mapeo
        acronym_map = {
            'AC': 'Active Competitor',
            'DNF': 'Did Not Finish',
            'DNQ': 'Did Not Qualify',
            'DNS': 'Did Not Start',
            'DQ': 'Disqualified',
            'EL': 'Eliminated',
            'HC': 'Hors Catégorie',
            'HM': 'Honourable Mention',
            'MNK': 'Shooting – Running Target, 50 metres, Men',
            'NH': 'No Height',
            'NM': 'No Mark',
            'NP': 'Not Placed',
            'NVL': 'No Valid Lift',
            'TNK': 'Athletics – 10,000 metres, Men'
        }

        # Reemplazo de los acrónimos con sus significados
        df_acron['Full Meaning'] = df_acron['Acronym'].map(acronym_map)
        st.markdown('####List of the acronimus:')
        st.table(df_acron)
