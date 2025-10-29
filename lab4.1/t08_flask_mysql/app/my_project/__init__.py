import os
import secrets
from pathlib import Path
from typing import Any, Dict, Optional

from flask import Flask
from flasgger import Swagger
from sqlalchemy_utils import database_exists, create_database
from t08_flask_mysql.app.my_project.route import register_routes
from .db import db

# Константи для конфігурації
SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"
MYSQL_SSL_CA = "MYSQL_SSL_CA"
MYSQL_SSL_MODE = "MYSQL_SSL_MODE"
SQLALCHEMY_ENGINE_OPTIONS = "SQLALCHEMY_ENGINE_OPTIONS"
DEFAULT_SSL_MODE = "REQUIRED"


def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    # Обробка вхідної конфігурації
    _process_input_config(app_config, additional_config)

    # Створення Flask додатку
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    # Об’єднання конфігурацій
    app.config.update(app_config)

    # Ініціалізація БД + маршрути
    _init_db(app)
    register_routes(app)

    # Swagger UI (/apidocs)
    Swagger(app)

    return app


def _init_db(app: Flask) -> None:
    db.init_app(app)

    # Створення бази даних, якщо не існує
    db_uri = app.config.get(SQLALCHEMY_DATABASE_URI)
    if db_uri and not database_exists(db_uri):
        create_database(db_uri)

    with app.app_context():
        db.create_all()


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    """
    Формує URI для SQLAlchemy з даних додаткової конфігурації та змінних оточення
    """
    root_user = os.getenv(MYSQL_ROOT_USER) or additional_config.get(MYSQL_ROOT_USER)
    root_password = os.getenv(MYSQL_ROOT_PASSWORD) or additional_config.get(MYSQL_ROOT_PASSWORD)

    if not root_user or not root_password:
        raise ValueError("MySQL root user and password must be provided in env or additional_config")

    db_template = app_config.get(SQLALCHEMY_DATABASE_URI)
    if not db_template:
        raise ValueError(f"{SQLALCHEMY_DATABASE_URI} must be defined in app_config")

    # Формуємо фінальний URI
    app_config[SQLALCHEMY_DATABASE_URI] = db_template.format(user=root_user, password=root_password)
    _configure_ssl(app_config, additional_config)


def _configure_ssl(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    ssl_ca_path = _resolve_config_value(MYSQL_SSL_CA, additional_config)
    ssl_mode = _resolve_config_value(MYSQL_SSL_MODE, additional_config, DEFAULT_SSL_MODE)

    if not ssl_ca_path:
        return

    ssl_path = Path(ssl_ca_path)
    if not ssl_path.exists():
        raise FileNotFoundError(f"SSL CA file not found at {ssl_ca_path}")

    engine_options = dict(app_config.get(SQLALCHEMY_ENGINE_OPTIONS, {}))
    connect_args = dict(engine_options.get("connect_args", {}))
    ssl_options = dict(connect_args.get("ssl", {}))

    ssl_options.setdefault("ca", ssl_ca_path)
    if ssl_mode:
        ssl_options.setdefault("ssl_mode", ssl_mode)

    connect_args["ssl"] = ssl_options
    engine_options["connect_args"] = connect_args
    app_config[SQLALCHEMY_ENGINE_OPTIONS] = engine_options


def _resolve_config_value(key: str, additional_config: Dict[str, Any], default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key) or additional_config.get(key) or default
