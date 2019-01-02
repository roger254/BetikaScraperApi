import requests
from flask_restplus import Resource

from ..utils.dto import GameDto
from ..service.game_service import get_a_game, get_all_games, get_games_by_country, get_games_by_league, \
    get_games_by_sport, extract_game_odds

api = GameDto.api
_game = GameDto.game


@api.route('/')
class GameList(Resource):
    @api.doc('list of all games')
    @api.marshal_list_with(_game, envelope='data')
    def get(self):
        """List all games"""
        return get_all_games()


@api.route('/game/<int:game_id>')
@api.param('game_id', 'Unique game id')
@api.response(404, 'No such game available')
class Game(Resource):
    @api.doc('Get all odds for a game')
    def get(self, game_id):
        """Get games of a certain sport"""
        game = get_a_game(game_id)

        odds_url = game.odds_url
        response_data = extract_game_odds(odds_url)
        if not game:
            api.abort(404)
        else:
            return response_data


@api.route('/country/<country>/league/<league>')
@api.param('country', 'The Country of the league')
@api.param('league', 'The league of the game')
@api.response(404, 'League not found')
class League(Resource):
    @api.doc('get games of a league')
    @api.marshal_list_with(_game)
    def get(self, country, league):
        """get a league games given its country and league"""
        games = get_games_by_league(country, league)
        if not games:
            api.abort(404)
        else:
            return games


@api.route('/sport/<sport>')
@api.param('sport', 'The kind of sport ie soccer')
@api.response(404, 'No such sports available')
class Sport(Resource):
    @api.doc('Get all games for the sport')
    @api.marshal_list_with(_game)
    def get(self, sport):
        """Get games of a certain sport"""
        games = get_games_by_sport(sport)
        if not games:
            api.abort(404)
        else:
            return games


@api.route('/country/<country>')
@api.param('country', 'Desired Country')
@api.response(404, 'No such country available')
class Country(Resource):
    @api.doc('Get all games for the country')
    @api.marshal_list_with(_game)
    def get(self, country):
        """Get games of a certain sport"""
        games = get_games_by_country(country)
        if not games:
            api.abort(404)
        else:
            return games
