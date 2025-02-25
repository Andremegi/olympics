from fastapi import FastAPI
from olympics_folder.simple_analyzer import desired_history
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
    print(desired_df.index.to_list())
    print(desired_df['total'].to_list())

    return {'countries': desired_df.index.to_list(),
            'total':desired_df['total'].to_list(),
            'gold': desired_df['gold'].to_list(),
            'silver': desired_df['silver'].to_list(),
            'bronze': desired_df['bronze'].to_list()}
