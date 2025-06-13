import json
import os

def load_db_config():
    config_path = os.path.join(os.path.dirname(__file__), 'appsettings.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['database_connection_settings']