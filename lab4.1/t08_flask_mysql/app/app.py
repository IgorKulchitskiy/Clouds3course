import sys
import os
import yaml
from waitress import serve
from t08_flask_mysql.app.my_project import create_app

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"

# --- Визначаємо середовище ---
flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

# --- Визначаємо корінь проєкту lab4.1 ---
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_yaml_path = os.path.join(base_dir, 'config', 'app.yml')

# --- Завантаження YAML ---
with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
    config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
    additional_config = config_data_dict[ADDITIONAL_CONFIG]

# --- Вибір конфігурації ---
config_data = config_data_dict[DEVELOPMENT] if flask_env == DEVELOPMENT else config_data_dict[PRODUCTION]

# --- Створення додатку ---
app = create_app(config_data, additional_config)

if __name__ == "__main__":
    if flask_env == DEVELOPMENT:
        # debug жорстко вкл.
        app.run(host=HOST, port=DEVELOPMENT_PORT, debug=True)
    else:
        serve(app, host=HOST, port=PRODUCTION_PORT)
