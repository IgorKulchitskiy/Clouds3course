from t08_flask_mysql.app.my_project.domain.user_game_ownership import UserGameOwnership
from t08_flask_mysql.app.my_project.db import db
from sqlalchemy import text
class UserGameOwnershipDAO:
    @staticmethod
    def get_all_ownerships():
        return UserGameOwnership.query.all()

    @staticmethod
    def get_ownership_by_id(ownership_id):
        return UserGameOwnership.query.get(ownership_id)

    @staticmethod
    def create_ownership(user_id, game_id, purchase_date=None):
        new_ownership = UserGameOwnership(UserID=user_id, GameID=game_id, PurchaseDate=purchase_date)
        db.session.add(new_ownership)
        db.session.commit()
        return new_ownership

    @staticmethod
    def delete_ownership(ownership_id):
        ownership = UserGameOwnership.query.get(ownership_id)
        if ownership:
            db.session.delete(ownership)
            db.session.commit()
            return True
        return False

    @staticmethod
    def link_user_to_game(username, game_name):
        sql = text("CALL LinkUserToGame(:username, :game_name)")
        db.session.execute(sql, {'username': username, 'game_name': game_name})
        db.session.commit()




