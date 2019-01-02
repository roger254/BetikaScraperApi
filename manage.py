import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.service.game_scraper import collect_games_details
from app.main.service.game_service import save_game_data

app = create_app(os.getenv('FLASK_ENV') or 'development')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def new_games():
    if os.path.exists('match_details.json'):
        os.remove('match_details.json')
    collect_games_details()
    save_game_data()


@manager.command
def test():
    """Run the tests"""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
