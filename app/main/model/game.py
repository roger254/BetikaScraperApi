from .. import db


class Game(db.Model):
    """Game model for storing game related details"""
    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    country = db.Column(db.String)
    sport = db.Column(db.String)
    league = db.Column(db.String)
    away_team = db.Column(db.String)
    home_team = db.Column(db.String)
    starting_time = db.Column(db.DateTime)
    game_id = db.Column(
        db.Integer,
        unique=True
    )
    odds_url = db.Column(
        db.String,
        unique=True
    )

    def __init__(self, country, sport, league, away_team, home_team, starting_time, game_id, odds_url):
        self.country = country
        self.sport = sport
        self.league = league
        self.away_team = away_team
        self.home_team = home_team
        self.game_id = game_id
        self.starting_time = starting_time
        self.odds_url = odds_url

    def __repr__(self):
        return "<Game '{}'".format(self.game_id)
