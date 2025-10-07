import os
import yaml
from waitress import serve
from t08_flask_mysql.app.my_project import create_app

DEVELOPMENT = "development"
PRODUCTION = "production"
HOST = "0.0.0.0"
DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080

# --- Визначаємо середовище ---
FLASK_ENV = os.environ.get("FLASK_ENV", DEVELOPMENT).lower()
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "1")  # <- заставляємо debug увімкнутися

# --- Корінь проєкту ---
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_yaml_path = os.path.join(base_dir, 'config', 'app.yml')

# --- Завантаження YAML ---
with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
    config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
    additional_config = config_data_dict["ADDITIONAL_CONFIG"]

# --- Вибір конфігурації ---
config_data = config_data_dict[DEVELOPMENT] if FLASK_ENV == DEVELOPMENT else config_data_dict[PRODUCTION]

# --- Створення додатку ---
app = create_app(config_data, additional_config)

# --- Вмикаємо debug глобально ---
if FLASK_ENV == DEVELOPMENT:
    app.debug = True
