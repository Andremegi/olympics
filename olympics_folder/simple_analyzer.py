import os
from datetime import datetime
import pandas as pd
import numpy as np
import re


# Adquiring relative path of this file
path = os.path.dirname(__file__)

# Path to documents
path_to_docs = os.path.join(path, 'documents')


event_results_df = pd.read_csv(f'{path_to_docs}/Olympic_Event_Results.csv', skipinitialspace=True)
athlete_event_detailed_df= pd.read_csv(f'{path_to_docs}/Olympic_Athlete_Event_Details.csv', skipinitialspace=True)
medal_history_df = pd.read_csv(f'{path_to_docs}/Olympic_Medal_Tally_History.csv', skipinitialspace=True)
athlete_biography_df = pd.read_csv(f'{path_to_docs}/Olympic_Athlete_Biography.csv', skipinitialspace=True)
games_summary_df= pd.read_csv(f'{path_to_docs}/Olympic_Games_Summary.csv', skipinitialspace=True)
country_profiles_df = pd.read_csv(f'{path_to_docs}/Olympic_Country_Profiles.csv', skipinitialspace=True)

def desired_history(desired_edition='Olympics',
                    initial_year = 1896,
                    final_year = datetime.today().year,
                    number_countries = 20):
    '''
    Creates an ordered list of the most medal winning countries
    regarding the edition , can be : Winter , Summer , Both (Olympics) or Intercalated
    (Special edition on 1906)
    '''
    # Create a variable containing the name of the edition you choose
    desired_edition_name= f'{desired_edition.lower()}_edition'

    # Creates the desired_medal history df regarding :
    # 1. The edition
    medal_history_df[desired_edition_name] = medal_history_df['edition'].apply(lambda row : desired_edition in row)
    desired_medal_history_df = medal_history_df[medal_history_df[desired_edition_name] == True]

    # 2. The years you want to be count
    desired_medal_history_df = desired_medal_history_df[(desired_medal_history_df['year']>=int(initial_year)) & (desired_medal_history_df['year']<= int(final_year)) ]


    # 3. Counts the number of medals per country , order in descending order and give as result the top number_countries param given
    medal_sum_df = desired_medal_history_df[['country_noc', 'total', 'gold', 'silver', 'bronze']].groupby('country_noc').sum().sort_values('total',ascending = False,ignore_index=False).head(int(number_countries))

    #countries = medal_sum_df.index.unique()

    return  medal_sum_df


def proportional_medals_athlets(desired_edition='Olympics',
                                 initial_year = 1896,
                                final_year = datetime.today().year,
                                number_countries = 20):
    """
    It checks the total number of athletes in each country previously
    obtained on the desired_history and checks the number of athlets they
    presented as country, as it might be a cause of winning more medals , and
    gives back the propottion of medals/athlets

    """
    #obtain edition name
    desired_edition_name= f'{desired_edition.lower()}_edition'
    # obatin the countries of interest
    medal_sum_df = desired_history(desired_edition, initial_year, final_year,number_countries )

    #merges datasets to get  the total number of  athlets that participate on the olympics
    athlete_biography_extended_df = athlete_biography_df.merge(athlete_event_detailed_df[['sport','event', 'edition', 'athlete_id']], how='left', on = 'athlete_id')

    #filter to get the athlets only from the seected edition
    athlete_biography_extended_df[desired_edition_name] = athlete_biography_extended_df['edition'].apply(lambda row : desired_edition in row)
    desired_athlete_biography_extended_df = athlete_biography_extended_df[athlete_biography_extended_df[desired_edition_name] == True]

    #Takes the number of athlets inside the number_countries per country
    countries = medal_sum_df.index.unique()

    #first_ath_country=[]
    for index, country in enumerate(countries):
        medal_sum_df.loc[index,'number_athlets']=desired_athlete_biography_extended_df[desired_athlete_biography_extended_df['country_noc'] == f'{country}'].shape[0]

        #first_ath_country.append(desired_athlete_biography_extended_df[desired_athlete_biography_extended_df['country_noc'] == f'{country}'].shape[0])

    #medal_sum_df['number_athlets']=first_ath_country
    #Creates the proportion
    medal_sum_df['proportion_medal_athletes']=medal_sum_df['total']/medal_sum_df['number_athlets']
    prop_medal_athlets_df = medal_sum_df.sort_values('proportion_medal_athletes', ascending=False)[['number_athlets', 'proportion_medal_athletes']]

    return prop_medal_athlets_df

def cleaning_top_athlets(df):
    # Replace Nan 0
    df['medal'] = df['medal'].fillna(0)
    #df = df.dropna()
    df = df.drop(columns='pos')
    df['points'] = df['medal'].map({'Bronze':1,'Silver':2, 'Gold':3, 0:0 })
    df['medal'] = df['medal'].map({'Bronze':1,'Silver':1, 'Gold':1, 0:0 })
    df['year']=df['edition'].apply(lambda row : int(row.split()[0]))
    return df

def country_athlete(athletes, df):
    """
    Get the actual country of each athlete
    """
    countries=[]
    for athlete in athletes:
        country=(df[df['athlete']== athlete][['country_noc']].iloc[0]['country_noc'])
        countries.append(country_profiles_df[country_profiles_df['noc']==country].iloc[0]['country'])
    return countries

def top3_athlete_category(sport='Athletics', category='1,500 metres, Men', initial_year=1896, final_year=2022):
    #getting info of the morphology of athlets and putting all together
    athlete_morphotype = athlete_biography_df[['athlete_id', 'sex', 'born', 'height', 'weight']]
    athlete_biography_extended2_df = athlete_event_detailed_df.merge(athlete_morphotype, how='left', on = 'athlete_id')

    #cleaning data
    clean_df = cleaning_top_athlets(athlete_biography_extended2_df)

    #Filter by year
    clean_df = clean_df[(clean_df['year'] >= int(initial_year)) & (clean_df['year']<= int(final_year)) ]

   #Filter 3-5 first athlets selon the sport and category regarding 1. their point (3 first, 2 second, 1 third) 2. their number of medals
   # Create 2 different df , 1. Athlets selon their number of medals, 2. Athlets selon their number of points
    num_medals_ath_cat = clean_df[(clean_df['sport']==sport) & (clean_df['event']==category)].groupby('athlete').sum().sort_values('medal', ascending = False).head(5)
    num_points_ath_cat = clean_df[(clean_df['sport']==sport) & (clean_df['event']==category)].groupby('athlete').sum().sort_values('points', ascending = False).head(5)

    # Get their country and add it to the corresponding df
    num_medals_ath_cat['country'] = country_athlete(num_medals_ath_cat.index.to_list(), clean_df)
    num_points_ath_cat['country'] = country_athlete(num_points_ath_cat.index.to_list(), clean_df)

    return num_medals_ath_cat[['medal', 'country']], num_points_ath_cat[['points', 'country']]

def country_con_noc(country_name):
    """
    Get the noc of country
    """
    country = country_profiles_df[country_profiles_df['noc'] == country_name].iloc[0]['country']
    return country

def country_to_noc(country_name):
    """
    Get the noc of country
    """
    country = country_profiles_df[country_profiles_df['country'] == country_name].iloc[0]['noc']
    return country

def country_evolution(country='USA'):
    """
    Gets the number of medals of a country since 1896 until 2022 so you can see the evolution
    """
    country_history_df = medal_history_df[(medal_history_df['country'] == country_con_noc(country))]
    country_history_df['editions'] = country_history_df['edition'].apply(lambda row : row.split()[1])
    country_history_df['year'] = country_history_df['year'].apply(lambda row : int(row))
    return country_history_df

def number_athlets(country='USA'):
    #num_ath=[]
    year_medals_per_country_df= country_evolution(country)

    #getting info of the morphology of athlets and putting all together
    #athlete_morphotype = athlete_biography_df[['athlete_id', 'sex', 'born', 'height', 'weight']]
    #athlete_biography_extended2_df = athlete_event_detailed_df.merge(athlete_morphotype, how='left', on = 'athlete_id')
    #cleaning data
    athlete_biography_extended2_df = cleaning_top_athlets(athlete_event_detailed_df)
    for index,year in enumerate(year_medals_per_country_df['year'].to_list()):
        year_medals_per_country_df.loc[index,'num_ath'] = athlete_biography_extended2_df[(athlete_biography_extended2_df['country_noc'] == country) & (athlete_biography_extended2_df['year'] == year)]['athlete_id'].nunique()

        #num_ath.append(athlete_biography_extended2_df[(athlete_biography_extended2_df['country_noc'] == country) & (athlete_biography_extended2_df['year'] == year)]['athlete_id'].nunique())
    #year_medals_per_country_df['num_ath']=num_ath
    #year_medals_per_country_df['editions']=year_medals_per_country_df['edition'].apply(lambda row : row.split()[1])

    return year_medals_per_country_df

def evolution_per_year(year=1896, country='USA'):
    #getting info of the morphology of athlets and putting all together
    #athlete_morphotype = athlete_biography_df[['athlete_id', 'sex', 'born', 'height', 'weight']]
    #athlete_biography_extended2_df = athlete_event_detailed_df.merge(athlete_morphotype, how='left', on = 'athlete_id')

    #cleaning data
    athlete_biography_extended2_df = cleaning_top_athlets(athlete_event_detailed_df)

    sports_medals_year = pd.DataFrame(athlete_biography_extended2_df[(athlete_biography_extended2_df['country_noc'] == country) & (athlete_biography_extended2_df['year'] == int(year))].groupby('sport').sum()['medal'])

    return sports_medals_year


def born_year(date):
    if type(date) == str:
        list_date = date.split()
        target = re.sub('[^0-9]','', list_date[-1])
        if ('1' in  target) or ('2' in target) :
            return int(target)
        else: return 0

    return int(date)


def clean_ath_datasets(df):
    #Fillna
    df['pos'] = df['pos'].fillna('-No information')
    df['medal'] = df['medal'].fillna(0)
    df['sex'] = df['sex'].fillna('-Not specified')
    df['height'] = df['height'].fillna('-Not specified')
    df['weight'] = df['weight'].fillna('-Not specified')
    df['born'] = df['born'].fillna(0)
    df['description'] = df['description'].fillna('-Not specified')
    df['special_notes'] = df['special_notes'].fillna('-Not specified')

    #Replacements
    df['pos'] = df['pos'].replace(['DNS','DNF', 'DQ'],['Did not start', 'Did not finish', 'Disqualified'])

    #New creations
    df['age'] = df.apply(lambda row:int(row['edition'][0:4]) - born_year(row['born']), axis=1)
    df['age'] = df['age'].apply(lambda row : '-Not specified' if row > 100 else row)

    return df.dropna()

def athlete(sport='Athletics', name='Usain Bolt'):
    #columns to drop and  dropping
    drop_cols_on_athlete_event_detailed={'edition_id', 'country_noc', 'result_id'}
    drop_cols_on_athlete_biography={ 'name', 'country_noc'}
    athlete_event_df = athlete_event_detailed_df.drop_duplicates()
    athlete_event_df = athlete_event_df.drop(columns=drop_cols_on_athlete_event_detailed)
    athlete_bio_df = athlete_biography_df.drop(columns=drop_cols_on_athlete_biography)

    #Merging to extract all the wanted info
    athlete_df = athlete_event_df.merge(athlete_bio_df, how ='left', on ='athlete_id')
    #athlete_df = athlete_df.drop(columns={'result_id','athlete_id'})

    #Cleaning
    athlete_clean_df = clean_ath_datasets(athlete_df)

    #Filtering on what we want
    athlete_info_df = athlete_clean_df [(athlete_clean_df['sport']==sport) & (athlete_clean_df['athlete']==name)]
    return athlete_info_df


#print(desired_history())
#print(proportional_medals_athlets())
#print(top3_athlete_category())
print(athlete())
