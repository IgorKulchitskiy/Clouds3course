from t08_flask_mysql.app.my_project.db import db
from t08_flask_mysql.app.my_project.domain.games import Game
from t08_flask_mysql.app.my_project.domain.users import User

class UserGameOwnership(db.Model):
    __tablename__ = 'UserGameOwnership'

    OwnershipID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    GameID = db.Column(db.Integer, db.ForeignKey('Games.GameID'), nullable=False)
    PurchaseDate = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Відношення
    user = db.relationship('User', back_populates='owned_games')
    game = db.relationship('Game', back_populates='owned_by_users')
