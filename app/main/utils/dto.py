from flask_restplus import Namespace, fields


class GameDto:
    api = Namespace('game', description='game related operations')
    game = api.model(
        'game',
        {
            'game_id': fields.Integer(description='unique game identifier'),
            'country': fields.String(description='Country the game resides'),
            'sport': fields.String(description='Type of sport'),
            'league': fields.String(description='League of the game'),
            'away_team': fields.String(description='Away team of the game'),
            'home_team': fields.String(description='Home team of the game'),
            'starting_time': fields.DateTime(description='Starting time of the game')
        }
    )


# class OddDto:
#     api = Namespace('odds', description='Odds for a specific game')
#     odds = api.model(
#         'odds',
#         {
#             'name': fields.String(description='name of the odd'),
#             ''
#         }
#     )
