from t08_flask_mysql.app.my_project.db import db

class Game(db.Model):
    __tablename__ = 'Games'

    GameID = db.Column(db.Integer, primary_key=True)
    GameName = db.Column(db.String(100), nullable=False)
    PublisherID = db.Column(db.Integer, db.ForeignKey('Publishers.PublisherID'), nullable=True)
    ReleaseDate = db.Column(db.Date)

    # Відношення до таблиці Publishers
    publisher = db.relationship('Publisher', back_populates='games')
    owned_by_users = db.relationship('UserGameOwnership', back_populates='game')

