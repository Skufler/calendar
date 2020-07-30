"""
    Configuration for app
"""
from pathlib import Path

from yaml import safe_load


BASE_DIR = Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config.yaml'


def load_config(config_path: Path) -> dict:
    """
    Load config from a given path.

    :param config_path:
    :return: config dict
    """
    with config_path.open() as config_file:
        cfg: dict = safe_load(config_file)

    return cfg


config = load_config(DEFAULT_CONFIG_PATH)
