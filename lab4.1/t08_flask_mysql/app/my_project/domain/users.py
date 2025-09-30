from t08_flask_mysql.app.my_project.db import db

class User(db.Model):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    RegistrationDate = db.Column(db.DateTime, default=db.func.current_timestamp())

    owned_games = db.relationship('UserGameOwnership', back_populates='user')

