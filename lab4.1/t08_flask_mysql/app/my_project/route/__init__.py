from t08_flask_mysql.app.my_project.controller.users_controller import users_bp
from t08_flask_mysql.app.my_project.controller.publishers_controller import publishers_bp
from t08_flask_mysql.app.my_project.controller.games_controller import games_bp
from t08_flask_mysql.app.my_project.controller.user_game_ownership_controller import user_game_bp

def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(publishers_bp, url_prefix='/publishers')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(user_game_bp, url_prefix='/user-game-ownership')

