import os

import yaml

def load_settings(section: str = "cyberdolphin"):
    path = os.path.join(os.path.dirname(__file__), "settings.yaml")
    with open(path) as settings:
        the_yaml = yaml.safe_load(settings)
    print(f"LOADED: {the_yaml[section]}")
    return the_yaml[section]
