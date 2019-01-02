import json

import requests

sports_url = 'https://api.betika.com/v1/uo/sports'


def sort_data(collected_data):
    game_id_list = set()
    index_list = []
    for x in collected_data:
        game_id = x['game_id']
        if game_id in game_id_list:
            index_list.append(collected_data.index(x))

        game_id_list.add(game_id)

    for index in sorted(index_list, reverse=True):
        del collected_data[index]

    return collected_data


def load_sports_details():
    response = requests.get(url=sports_url)
    response_data = response.json().get('data')

    return_data = []

    for data in response_data:
        data_dict = {}
        data_dict['sport_id'] = data['sport_id']
        data_dict['sport_name'] = data['sport_name']
        categories = data['categories']
        country_list = []
        for category in categories:
            country_data = {}
            country_data['country_name'] = category['category_name']
            country_data['country_id'] = category['category_id']
            country_leagues = []
            leagues = category['competitions']
            for league in leagues:
                league_details = {}
                league_details['league_name'] = league['competition_name']
                league_details['League_id'] = league['competition_id']
                country_leagues.append(league_details)
            country_data['leagues'] = country_leagues
            country_list.append(country_data)
        data_dict['country'] = country_list
        return_data.append(data_dict)

    with open('sports_details.json', 'w') as outfile:
        json.dump(return_data, outfile)
    return return_data


def load_match_urls():
    match_url_set = set()
    response = requests.get(url=sports_url)
    data = response.json().get('data')

    print("Collecting match urls")
    for sports in data:
        sport_id = sports['sport_id']
        categories = sports['categories']

        for cat in categories:
            competitions = cat['competitions']
            for competition in competitions:
                competition_id = competition['competition_id']
                match_url = 'https://api.betika.com/v1/uo/matches?sport_id=%s&competition_id=%s' \
                            '&tab=upcoming&sub_type_id=1,186' % (sport_id, competition_id)
                match_url_set.add(match_url)

        # if sport_id and competition_id_list is not None:
        #     # if int(sport_id) == 14:
        #     print('here')
        #     for competition_id in competition_id_list:
        #         match_url = 'https://api.betika.com/v1/uo/matches?sport_id=%s&competition_id=%s' \
        #                     '&tab=upcoming&sub_type_id=1,186' % (sport_id, competition_id)
        #         match_url_list.append(match_url)

    print('Collected match urls')
    match_url_list = list(match_url_set)
    return match_url_list


def collect_games_details():
    matches_url = load_match_urls()
    return_data = []
    print('Collection games url and start data')

    for url in matches_url:
        print(url)

        response = requests.get(url=url)
        if response.status_code != 200:
            print('Missed')
            continue
        games = response.json().get('data')
        if len(games) > 0:

            for game in games:
                data_dict = {}
                game_id = int(game['game_id'])
                data_dict['game_id'] = game_id
                match_id = game['match_id']
                data_dict['home_team'] = game['home_team']
                data_dict['away_team'] = game['away_team']
                data_dict['starting_time'] = game['start_time']
                data_dict['league_name'] = game['competition_name']
                data_dict['competition_id'] = game['competition_id']
                data_dict['country'] = game['category']
                data_dict['sport_name'] = game['sport_name']
                data_dict['odds_url'] = 'https://api.betika.com/v1/uo/match?id=%s' % match_id

                return_data.append(data_dict)

    # return_data = sort_data(return_data)

    with open('match_details.json', 'w') as outfile:
        json.dump(return_data, outfile)
    return return_data

# collect_games_detials()
