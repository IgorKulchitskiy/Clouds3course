from t08_flask_mysql.app.my_project.dao.user_game_ownership_dao import UserGameOwnershipDAO

class UserGameOwnershipService:
    @staticmethod
    def get_all_ownerships():
        return UserGameOwnershipDAO.get_all_ownerships()

    @staticmethod
    def get_ownership_by_id(ownership_id):
        return UserGameOwnershipDAO.get_ownership_by_id(ownership_id)

    @staticmethod
    def create_ownership(user_id, game_id, purchase_date=None):
        return UserGameOwnershipDAO.create_ownership(user_id, game_id, purchase_date)

    @staticmethod
    def delete_ownership(ownership_id):
        return UserGameOwnershipDAO.delete_ownership(ownership_id)

    @staticmethod
    def link_user_to_game(username, game_name):
        UserGameOwnershipDAO.link_user_to_game(username, game_name)
