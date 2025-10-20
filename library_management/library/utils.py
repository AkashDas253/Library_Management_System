import configparser
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')

def get_auto_accept_virtual():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        return False
    config.read(CONFIG_PATH)
    try:
        return config.getboolean('Borrow', 'auto_accept_virtual', fallback=False)
    except Exception:
        return False
