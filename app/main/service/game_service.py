import json
from datetime import datetime

import requests

from app.main import db
from app.main.model.game import Game


def save_game_data():
    db.drop_all()
    db.create_all()
    loaded_data = load_data('match_details')
    game_list = []
    for data in loaded_data:
        game_id = data['game_id']
        country = data['country']
        sport = data['sport_name']
        league = data['league_name']
        away_team = data['away_team']
        home_team = data['home_team']
        starting_time = extract_time(data['starting_time'])
        odds_url = data['odds_url']
        game = Game(
            game_id=game_id,
            country=country,
            sport=sport,
            league=league,
            away_team=away_team,
            home_team=home_team,
            starting_time=starting_time,
            odds_url=odds_url)
        game_list.append(game)

    db.session.add_all(game_list)
    db.session.commit()
    db.session.close()


def get_all_games():
    return Game.query.all()


def get_a_game(game_id):
    return Game.query.filter_by(game_id=game_id).first()


def get_games_by_country(country):
    return Game.query.filter_by(country=country).all()


def get_games_by_sport(sport):
    return Game.query.filter_by(sport=sport).all()


def get_games_by_league(country, league):
    return Game.query.filter_by(country=country, league=league).all()


def load_data(file_name):
    with open(file_name + '.json') as f:
        collected_data = json.load(f)
    return collected_data


def extract_time(param):
    date, time = param.split(" ")
    year, month, day = date.split("-")
    hours, minutes, seconds = time.split(":")
    return datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=int(hours),
        minute=int(minutes),
        second=int(seconds)
    )


def extract_game_odds(odds_url):
    response = requests.get(url=odds_url)
    response_data = response.json().get('data')

    return_data = []
    for data in response_data:
        odd_data = {}
        odd_data['name'] = data['name']
        odds = data['odds']
        odd_info = []
        for odd in odds:
            odds_dict = {}
            odds_dict['display'] = odd['display']
            odds_dict['key'] = odd['odd_key']
            odds_dict['value'] = odd['odd_value']
            odd_info.append(odds_dict)
        odd_data['odds'] = odd_info
        return_data.append(odd_data)

    return return_data
