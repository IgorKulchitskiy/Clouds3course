from t08_flask_mysql.app.my_project.db import db

class Publisher(db.Model):
    __tablename__ = 'Publishers'

    PublisherID = db.Column(db.Integer, primary_key=True)
    PublisherName = db.Column(db.String(100), nullable=False)

    # Відношення до таблиці Games
    games = db.relationship('Game', back_populates='publisher', lazy=True)
