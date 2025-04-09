import streamlit as st
import requests
import pandas as pd


st.markdown("""
    ### Compare the number of medals each country won according to :
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
#params to automatize the year change on  initial and last year
first_year=1896
last_year=2023
number = 20

if option =='Intercalated':
    first_year=1906
    last_year=1907
    number = 17
    st.markdown(f'**Intercalted** is a special edition cariied out in **1906** where only **17** countries compited')

if option =='Equestrian':
    first_year=1956
    last_year=1957
    number = 7
    st.markdown(f'**Intercalted** is a special edition cariied out in **1956** where only **7** countries compited ')

initial_year = col2.selectbox('Initial year', range(first_year,last_year))
final_year = col3.selectbox('Final year', range(initial_year,last_year))
number_countries = col4.text_input('Number of countries', number)


buton = st.button('Compare')
url_railways = 'https://olympics-production-247f.up.railway.app/best_countries?'
#url_render = 'https://olympiastats.onrender.com/best_countries?'
#url = 'http://127.0.0.1:8000/best_countries?'

if buton :
    params = {'desired_edition': option,
              'initial_year': initial_year,
              'final_year': final_year,
              'number_countries': number_countries}

    response = requests.get(url_railways, params=params)
    #response.raise_for_status()  # raises exception when not a 2xx response
    if str(response.status_code)[0] in '45':
        st.markdown(f'# Error {response.status_code}, please reload the window')
    if response.status_code != 204:
        response = response.json()
        if len(response['best_countries']) < int(number_countries):
            number_countries = len(response['best_countries'])
            st.markdown(f'In this case only **{number_countries}** participated...')

        medal = ['#FFD700', '#C0C0C0',  '#B8860B']

        #Create dataframe to be able to plot with st(with more info) and then create comparative tables
        df = pd.DataFrame.from_dict(response)
        sorted = df.sort_values('total', ascending = False)
        sorted_non_spaces = sorted.copy()
        i=0
        for l,country in sorted[['best_countries']].iterrows():
            sorted.loc[i,'best_countries'] = f'{country[0].rjust(int(number_countries)+10 - i)}'
            i += 1
        sorted.rename(columns={'best_countries':'Country'}, inplace = True)
        df = sorted.set_index('Country')
        df =df[['gold','silver','bronze']]
        df.columns = ['1.Gold', '2.Silver', '3.Bronze']

        st.markdown(f'In the next chart it is represented the number *(as value in the chart)* of gold, silver and bronze medals *(as color in the chart)* from the best **{number_countries}** countires in **descending** order')
        st.markdown("""### MEDALS PER COUNTRY""")

        st.bar_chart(df, color = medal, x_label=f'Top {number_countries} countries', y_label='Number of medals')

        sorted_non_spaces['medal/athletes best countries'] = response['proport_countries']

        # you need to caal to the API so your function is recognised
        #url_con_noc ='http://127.0.0.1:8000/list_country_names?'
        #url_country_list_render ='https://olympiastats.onrender.com/list_country_names?'
        url_country_list_railways = 'https://olympics-production-247f.up.railway.app/list_country_names?'

        #1. for the best countries
        # Before , to much processes, sorted_non_spaces[f'Top {number_countries} countries'] = sorted_non_spaces['best_countries'].apply(lambda row : requests.get(url_country_name_render, params = {'argument':row }).json()['name'])
        sorted_non_spaces[f'Top {number_countries} countries'] = requests.get(url_country_list_railways, params = {'list': sorted_non_spaces['best_countries'].to_list()}).json()['list']

        # 2. for the medal athlets ratio
        # Before sorted_non_spaces[f'Ratio medal/athletes'] = sorted_non_spaces['medal/athletes best countries'].apply(lambda row : requests.get(url_country_name_render, params = {'argument':row }).json()['name'])
        sorted_non_spaces[f'Ratio medal/athletes'] = requests.get(url_country_list_railways, params = {'list': sorted_non_spaces['medal/athletes best countries'].to_list()}).json()['list']

        st.markdown(f'Bellow we compare the first **{number_countries}** countries in **descending** order, regarding:')

        st.markdown(f'- The first column *Top {number_countries} countries* represents the best countries regarding their total number of medals')
        st.markdown(f'- The second column *Ratio medal/athletes*  represents a ratio between the total number of medals and the total number of athlets each country has')

        st.table(sorted_non_spaces[[f'Top {number_countries} countries', f'Ratio medal/athletes' ]])
