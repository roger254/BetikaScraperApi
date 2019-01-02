from flask_restplus import Api
from flask import Blueprint

from .main.controller.game_controller import api as game_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Betika Odds Scraper Api',
    version='1.0',
    description='An API from scrapped odds from betika webiste'
)

api.add_namespace(game_ns, path='/game')
