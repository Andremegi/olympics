import streamlit as st
from  datetime import datetime
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import os

def blank_space(df, names):
    i=1
    for l,name in df[[names]].iterrows():
        df.loc[l,names] = f'{i}.{name[0]}'

        print(name[0])
        i += 1
    return df

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to documents
path_to_docs = os.path.join(path, '..','..','olympics_folder','documents')
athlete_event_detailed_df = pd.read_csv(f'{path_to_docs}/Olympic_Athlete_Event_Details.csv', skipinitialspace=True)
sports= athlete_event_detailed_df['sport'].unique()


st.markdown("""

    ### Here you can check the best **5** athlets in any sport and category of your choice

""")

col1, col2, col3, col4 = st.columns(4)
sport = col1.selectbox('Select sport', sports)

#Create the category regarding the sport
cat = athlete_event_detailed_df[athlete_event_detailed_df['sport']==sport]['event'].unique()
category = col2.selectbox('Select category',cat )
initial_year = col3.selectbox('Initial year', range(1896,2023))
final_year = col4.selectbox('Final year', range(initial_year,2023))

url_render = 'https://olympiastats.onrender.com/best_athlets?'
#url ='http://127.0.0.1:8000/best_athlets'
params = {'sport':sport,
          'category':category,
          'initial_year':initial_year,
          'final_year':final_year}

buton = st.button('Analyze')
if buton:
    response = requests.get(url_render, params=params).json()
    df_medal = pd.DataFrame.from_dict(response[0]).sort_values('num_medals', ascending =False)
    df_points = pd.DataFrame.from_dict(response[1]).sort_values('num_points', ascending=False)


    df_medal = blank_space(df_medal,'top5_medal_athlets')
    df_points = blank_space(df_points,'top5_points_athlets')
    df_medal.rename(columns={'medal_athlets_country':'Countries'}, inplace =True)
    df_points.rename(columns={'points_athlets_country':'Countries'}, inplace =True)

    st.markdown("""
                ### Regarding their **number of medals**
                """)
    st.markdown(f'Please note that its posible that there are more athlets with the same number of medals')

    st.bar_chart(df_medal,
                 x= 'top5_medal_athlets',
                 y='num_medals',
                 color = 'Countries',
                 x_label='Top 5 athlets',
                 y_label='Number of medals')

    st.markdown("""
                ### Regarding their **points**
                """)
    st.markdown("""
                The points are stipulated like :
                - **3** points for the **first** position
                - **2** points for the **second** position
                - **1** point for the **third** position
                """)

    st.bar_chart(df_points,
                 x= 'top5_points_athlets',
                 y='num_points',
                 color = 'Countries',
                 x_label = 'Top 5 athlets',
                 y_label = 'Number of points')
