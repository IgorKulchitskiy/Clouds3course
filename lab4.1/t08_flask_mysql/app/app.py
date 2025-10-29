import os
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

from flask import Flask
from t08_flask_mysql.app.my_project import create_app

ENVIRONMENT_VARIABLE = "FLASK_ENV"
DEVELOPMENT_ENVIRONMENT = "development"
PRODUCTION_ENVIRONMENT = "production"
ADDITIONAL_CONFIG_SECTION = "ADDITIONAL_CONFIG"
CONFIG_RELATIVE_PATH = Path(__file__).resolve().parents[2] / "config" / "app.yml"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_DEVELOPMENT_PORT = 5000


def _load_config() -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    environment = os.getenv(ENVIRONMENT_VARIABLE, DEVELOPMENT_ENVIRONMENT).lower()
    config_payload = _read_yaml(CONFIG_RELATIVE_PATH)
    environment_config, additional_config = _select_environment_config(config_payload, environment)
    return environment_config, additional_config, environment


def _read_yaml(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file) or {}


def _select_environment_config(config_payload: Dict[str, Any], environment: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if environment in config_payload:
        environment_config = config_payload[environment]
    elif PRODUCTION_ENVIRONMENT in config_payload:
        environment_config = config_payload[PRODUCTION_ENVIRONMENT]
    else:
        raise ValueError(f"Unsupported FLASK_ENV '{environment}' in {CONFIG_RELATIVE_PATH}")

    additional_config = config_payload.get(ADDITIONAL_CONFIG_SECTION, {})
    return environment_config, additional_config


def _build_application() -> Flask:
    app_config, additional_config, environment = _load_config()
    application = create_app(app_config, additional_config)

    if environment == DEVELOPMENT_ENVIRONMENT:
        application.debug = True

    return application


app = _build_application()


if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=DEFAULT_DEVELOPMENT_PORT, debug=app.debug)
