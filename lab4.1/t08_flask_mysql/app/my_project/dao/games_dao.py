from t08_flask_mysql.app.my_project.domain.games import Game
from t08_flask_mysql.app.my_project.db import db
from sqlalchemy import text
from sqlalchemy import func
class GamesDAO:
    @staticmethod
    def get_all_games():
        return Game.query.all()

    @staticmethod
    def get_game_by_id(game_id):
        return Game.query.get(game_id)

    @staticmethod
    def create_game(game_name, publisher_id, release_date):
        new_game = Game(GameName=game_name, PublisherID=publisher_id, ReleaseDate=release_date)
        db.session.add(new_game)
        db.session.commit()
        return new_game

    @staticmethod
    def update_game(game_id, game_name, publisher_id, release_date):
        game = Game.query.get(game_id)
        if game:
            game.GameName = game_name
            game.PublisherID = publisher_id
            game.ReleaseDate = release_date
            db.session.commit()
            return game
        return None

    @staticmethod
    def delete_game(game_id):
        game = Game.query.get(game_id)
        if game:
            db.session.delete(game)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_game_name_statistics(operation):
        valid_operations = {
            'MIN': func.min(func.length(Game.GameName)),
            'MAX': func.max(func.length(Game.GameName)),
            'AVG': func.avg(func.length(Game.GameName)),
            'COUNT': func.count(Game.GameName)
        }

        if operation.upper() not in valid_operations:
            raise ValueError(f"Invalid operation: {operation}. Use MIN, MAX, AVG, or COUNT.")

        result = db.session.query(valid_operations[operation.upper()]).scalar()
        return result

    @staticmethod
    def execute_create_random_game_tables():
        # Викликаємо збережену процедуру
        sql = text("CALL create_random_game_tables()")
        db.session.execute(sql)
        db.session.commit()