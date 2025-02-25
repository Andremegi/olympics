import os
from datetime import datetime
import pandas as pd
import numpy as np

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

print(datetime.today().year)
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

print(desired_history())
