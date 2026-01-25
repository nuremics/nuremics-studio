import json
import base64
import pandas as pd
from pathlib import Path
from platformdirs import user_config_path

from nuremics import Application

CONFIG_PATH = user_config_path(
    appname="nuRemics",
    appauthor=False,
)
SETTINGS_FILE: Path = CONFIG_PATH / "settings.json"


def image_to_data_url(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def get_app_features(
    app_name: str,
):
    app_features = {
        "import": None,
        "link": None,
        "visual": None,
        "logo": None,
        "color": None,
    }
    if app_name == "DEMO_APP":
        app_features["import"] = "general.DEMO_APP"
        app_features["link"] = "https://nuremics.github.io/labs/apps/general/DEMO_APP"
        app_features["visual"] = "https://raw.githubusercontent.com/nuremics/nuremics-docs/main/docs/images/DEMO_APP.png"
        app_features["logo"] = "https://raw.githubusercontent.com/nuremics/nuremics-docs/main/docs/images/logo.png"
        app_features["color"] = "#0080ff6f"

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


def get_studies(
    working_path: Path,
):
    studies_file: Path = working_path / "studies.json"
    with open(studies_file) as f:
        dict_studies = json.load(f)
    
    return dict_studies


def update_studies(
    working_path: Path,
    dict_studies: dict,
):
    studies_file: Path = working_path / "studies.json"
    with open(studies_file, "w") as f:
        json.dump(dict_studies, f, indent=4)


def update_list_studies(
    working_path: Path,
    list_studies: list,
):
    studies_file: Path = working_path / "studies.json"
    with open(studies_file) as f:
        dict_studies = json.load(f)

    dict_studies["studies"] = list_studies
    with open(studies_file, "w") as f:
        json.dump(dict_studies, f, indent=4)


def get_json_inputs(
    working_path: Path,
    study: str,
):
    inputs_file: Path = working_path / f"{study}/inputs.json"
    with open(inputs_file) as f:
        dict_inputs = json.load(f)
    
    return dict_inputs


def get_csv_inputs(
    app: Application,
    working_path: Path,
    study: str,
):
    inputs_file: Path = working_path / f"{study}/inputs.csv"
    
    if inputs_file.exists():
        df_inputs_col = pd.read_csv(inputs_file, nrows=0)
        
        dtypes = {
            "ID": "string",
            "EXECUTE": "int64",
        }
        for col in df_inputs_col.columns[1:-1]:
            if app.workflow.params_type[col][1] == "int":
                dtypes[col] = "int64"
            if app.workflow.params_type[col][1] == "float":
                dtypes[col] = "float64"
            if app.workflow.params_type[col][1] == "bool":
                dtypes[col] = "bool"
            if app.workflow.params_type[col][1] == "str":
                dtypes[col] = "string"
        
        df_inputs = pd.read_csv(inputs_file, dtype=dtypes)
    
    else:
        df_inputs = None

    return df_inputs