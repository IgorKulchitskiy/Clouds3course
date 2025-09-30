from t08_flask_mysql.app.my_project.domain.publisher import Publisher
from t08_flask_mysql.app.my_project.db import db

class PublishersDAO:
    @staticmethod
    def get_all_publishers():
        return Publisher.query.all()

    @staticmethod
    def get_publisher_by_id(publisher_id):
        return Publisher.query.get(publisher_id)

    @staticmethod
    def create_publisher(publisher_name):
        new_publisher = Publisher(PublisherName=publisher_name)
        db.session.add(new_publisher)
        db.session.commit()
        return new_publisher

    @staticmethod
    def update_publisher(publisher_id, publisher_name):
        publisher = Publisher.query.get(publisher_id)
        if publisher:
            publisher.PublisherName = publisher_name
            db.session.commit()
            return publisher
        return None

    @staticmethod
    def delete_publisher(publisher_id):
        publisher = Publisher.query.get(publisher_id)
        if publisher:
            db.session.delete(publisher)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_games_by_publisher(publisher_id):
        publisher = Publisher.query.get(publisher_id)
        if publisher:
            return publisher.games
        return None
