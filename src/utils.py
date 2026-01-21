import json
from platformdirs import user_config_path

CONFIG_PATH = user_config_path(
    appname="nuRemics",
    appauthor=False,
)
SETTINGS_FILE = CONFIG_PATH / "settings.json"


def get_app_features(
    app_name: str,
):
    app_features = {
        "import": None,
        "link": None,
        "visual": None,
    }
    if app_name == "DEMO_APP":
        app_features["import"] = "general.DEMO_APP"
        app_features["link"] = "https://nuremics.github.io/labs/apps/general/DEMO_APP"
        app_features["visual"] = "https://raw.githubusercontent.com/nuremics/nuremics-docs/main/docs/images/DEMO_APP.png"

    return app_features


def get_settings():
    with open(SETTINGS_FILE) as f:
        dict_settings = json.load(f)
    
    return dict_settings


def update_settings(
    dict_settings: dict
):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(dict_settings, f, indent=4)