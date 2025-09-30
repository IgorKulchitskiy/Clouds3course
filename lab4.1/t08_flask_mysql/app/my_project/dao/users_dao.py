from t08_flask_mysql.app.my_project.domain.users import User
from t08_flask_mysql.app.my_project.db import db
from sqlalchemy import text

class UsersDAO:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, email, password_hash):
        new_user = User(Username=username, Email=email, PasswordHash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, username, email, password_hash):
        user = User.query.get(user_id)
        if user:
            user.Username = username
            user.Email = email
            user.PasswordHash = password_hash
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def create_user_via_procedure(username, email, password_hash):
        sql = text("CALL InsertUser(:username, :email, :passwordHash)")
        db.session.execute(sql, {"username": username, "email": email, "passwordHash": password_hash})
        db.session.commit()