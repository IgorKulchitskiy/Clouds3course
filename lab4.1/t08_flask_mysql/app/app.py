import sys
import os
from waitress import serve
import yaml

from t08_flask_mysql.app.my_project import create_app

# --- Константи ---
DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"

if __name__ == '__main__':
    flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

    # --- Визначаємо корінь проєкту lab4.1 ---
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # --- Шлях до app.yml ---
    config_yaml_path = os.path.join(base_dir, 'config', 'app.yml')

    # --- Завантаження YAML ---
    with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
        config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
        additional_config = config_data_dict[ADDITIONAL_CONFIG]

        if flask_env == DEVELOPMENT:
            config_data = config_data_dict[DEVELOPMENT]
            app = create_app(config_data, additional_config)
            print("🚀 Flask running in DEVELOPMENT mode with debug=True")
            app.run(host=HOST, port=DEVELOPMENT_PORT, debug=True, use_reloader=True)

        elif flask_env == PRODUCTION:
            config_data = config_data_dict[PRODUCTION]
            app = create_app(config_data, additional_config)
            print("🌐 Flask running in PRODUCTION mode via Waitress")
            serve(app, host=HOST, port=PRODUCTION_PORT)

        else:
            raise ValueError(f"Check OS environment variable '{FLASK_ENV}'")
