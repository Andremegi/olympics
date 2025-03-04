from fastapi import FastAPI
from olympics_folder.simple_analyzer import desired_history, proportional_medals_athlets, top3_athlete_category, country_evolution, number_athlets
from olympics_folder.simple_analyzer import evolution_per_year
from datetime import datetime
app = FastAPI()

@app.get('/')
def root():
    return {'Olympians say': 'VAMOS!'}

@app.get('/best_countries')
def best_countries(desired_edition='Olympics',
                    initial_year = 1896,
                    final_year = datetime.today().year,
                    number_countries =20):
    desired_df = desired_history(desired_edition, initial_year, final_year, number_countries)
    #print(desired_df.index.to_list())
    #print(desired_df['total'].to_list())
    proportional_df = proportional_medals_athlets(desired_edition,initial_year ,final_year ,number_countries)

    return {'best_countries': desired_df.index.to_list(),
            'total':desired_df['total'].to_list(),
            'gold': desired_df['gold'].to_list(),
            'silver': desired_df['silver'].to_list(),
            'bronze': desired_df['bronze'].to_list(),
            'proport_countries':proportional_df.index.to_list()}

@app.get('/best_athlets')
def best_athlets(sport='Athletics',
                 category='1,500 metres, Men',
                 initial_year=1896,
                 final_year=2022):
    desired_medal_info, desired_points_info  = top3_athlete_category(sport, category, initial_year, final_year)
    return [{'top5_medal_athlets':desired_medal_info.index.to_list(),
            'num_medals':desired_medal_info['medal'].to_list(),
            'medal_athlets_country': desired_medal_info['country'].to_list()},
            {'top5_points_athlets':desired_points_info.index.to_list(),
            'num_points':desired_points_info['points'].to_list(),
            'points_athlets_country': desired_points_info['country'].to_list()}]

@app.get('/country_evolution')
def country_evolution_api(country_noc='USA'):
    desired_country_evolution = country_evolution(country_noc)
    desired_table_info = number_athlets(country_noc)

    return [{'year':desired_country_evolution['year'].to_list(),
            'total':desired_country_evolution['total'].to_list(),
            'edition': desired_country_evolution['editions'].to_list(),
            'country': desired_country_evolution['country'].to_list()},
           {'year':desired_table_info['year'].to_list(),
            'edition': desired_table_info['editions'].to_list(),
            'total':desired_table_info['total'].to_list(),
            'gold': desired_table_info['gold'].to_list(),
            'silver': desired_table_info['silver'].to_list(),
            'bronze': desired_table_info['bronze'].to_list(),
            'num_ath': desired_table_info['num_ath'].to_list()
            }]

@app.get('/deeper_country_evolution')
def deeper_country_evolution_api(year=1896, country_noc='USA'):
    evolution_df = evolution_per_year(str(year), country_noc)
    print(evolution_df)
    return {'sport': evolution_df.index.to_list(),
            'number_medals':evolution_df['medal'].to_list()}
