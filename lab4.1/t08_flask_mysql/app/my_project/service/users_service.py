from t08_flask_mysql.app.my_project.dao.users_dao import UsersDAO

class UsersService:
    @staticmethod
    def get_all_users():
        return UsersDAO.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UsersDAO.get_user_by_id(user_id)

    @staticmethod
    def create_user(username, email, password_hash):
        return UsersDAO.create_user(username, email, password_hash)

    @staticmethod
    def update_user(user_id, username, email, password_hash):
        return UsersDAO.update_user(user_id, username, email, password_hash)

    @staticmethod
    def delete_user(user_id):
        return UsersDAO.delete_user(user_id)

    @staticmethod
    def create_user_via_procedure(username, email, password_hash):
        UsersDAO.create_user_via_procedure(username, email, password_hash)
