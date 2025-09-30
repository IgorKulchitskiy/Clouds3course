from t08_flask_mysql.app.my_project.dao.publishers_dao import PublishersDAO
from sqlalchemy import text
from t08_flask_mysql.app.my_project.db import db

class PublishersService:
    @staticmethod
    def get_all_publishers():
        return PublishersDAO.get_all_publishers()

    @staticmethod
    def get_publisher_by_id(publisher_id):
        return PublishersDAO.get_publisher_by_id(publisher_id)

    @staticmethod
    def create_publisher(publisher_name):
        return PublishersDAO.create_publisher(publisher_name)

    @staticmethod
    def update_publisher(publisher_id, publisher_name):
        return PublishersDAO.update_publisher(publisher_id, publisher_name)

    @staticmethod
    def delete_publisher(publisher_id):
        return PublishersDAO.delete_publisher(publisher_id)

    @staticmethod
    def get_games_by_publisher(publisher_id):
        return PublishersDAO.get_games_by_publisher(publisher_id)

    @staticmethod
    def create_noname_publishers(start_num):
        sql = text("CALL InsertNonamePublishers(:startNum)")
        db.session.execute(sql, {"startNum": start_num})
        db.session.commit()