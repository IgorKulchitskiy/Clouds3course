from t08_flask_mysql.app.my_project.dao.games_dao import GamesDAO

class GamesService:
    @staticmethod
    def get_all_games():
        return GamesDAO.get_all_games()

    @staticmethod
    def get_game_by_id(game_id):
        return GamesDAO.get_game_by_id(game_id)

    @staticmethod
    def create_game(game_name, publisher_id, release_date):
        return GamesDAO.create_game(game_name, publisher_id, release_date)

    @staticmethod
    def update_game(game_id, game_name, publisher_id, release_date):
        return GamesDAO.update_game(game_id, game_name, publisher_id, release_date)

    @staticmethod
    def delete_game(game_id):
        return GamesDAO.delete_game(game_id)

    @staticmethod
    def get_game_name_statistics(operation):
        return GamesDAO.get_game_name_statistics(operation)

    @staticmethod
    def create_random_game_tables():
        # Використовуємо DAO для виконання процедури
        GamesDAO.execute_create_random_game_tables()
