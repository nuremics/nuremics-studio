import json
import copy
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


def update_dict_studies(
    dict_studies: dict,
    dict_config_wgt: dict,
):
    dict_studies_configured = copy.deepcopy(dict_studies)
    for key, value in dict_studies["config"].items():

        dict_studies_configured["config"][key]["execute"] = dict_config_wgt[key]["execute"].value
        
        for k, _ in value["user_params"].items():
            dict_studies_configured["config"][key]["user_params"][k] = dict_config_wgt[key]["user_params"][k].value
        for k, _ in value["user_paths"].items():
            dict_studies_configured["config"][key]["user_paths"][k] = dict_config_wgt[key]["user_paths"][k].value

    return dict_studies_configured


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


def get_json_file(
    working_path: Path,
    study: str,
    file_prefix: str,
):
    file_path: Path = working_path / f"{study}/{file_prefix}.json"
    if file_path.exists():
        with open(file_path) as f:
            dict = json.load(f)
    else:
        dict = None
    
    return dict


def update_json_file(
    dict: dict,
    working_path: Path,
    study: str,
    file_prefix: str,
):
    file_path: Path = working_path / f"{study}/{file_prefix}.json"
    with open(file_path, "w") as f:
        json.dump(dict, f, indent=4)


def get_inputs_csv(
    app: Application,
    working_path: Path,
    study: str,
):
    inputs_file: Path = working_path / f"{study}/inputs.csv"
    
    if inputs_file.exists():
        df_inputs_col = pd.read_csv(inputs_file, nrows=0)
        
        dtypes = {
            "ID": "string",
            "EXECUTE": "Int64",
        }
        for col in df_inputs_col.columns[1:-1]:
            if app.workflow.params_type[col][1] == "int":
                dtypes[col] = "Int64"
            if app.workflow.params_type[col][1] == "float":
                dtypes[col] = "float64"
            if app.workflow.params_type[col][1] == "bool":
                dtypes[col] = "boolean"
            if app.workflow.params_type[col][1] == "str":
                dtypes[col] = "string"
        
        df_inputs = pd.read_csv(inputs_file, dtype=dtypes)
    
    else:
        df_inputs = None

    return df_inputs


def update_inputs_csv(
    df_inputs: pd.DataFrame,
    working_path: Path,
    study: str,    
):
    inputs_file: Path = working_path / f"{study}/inputs.csv"
    df_inputs.to_csv(
        path_or_buf=inputs_file,
        index=False,
    )


def update_datasets(
    app: Application,
    dict_datasets_wgt: dict,
    working_path: Path,
):
    datasets = dict_datasets_wgt["datasets"]
    if datasets is not None:
        for col in datasets.value.columns:
            
            df_inputs = get_inputs_csv(
                app=app,
                working_path=working_path,
                study=col,
            )
            
            list_datasets = [x for x in datasets.value[col].to_list() if x]
            for dataset in list_datasets:
                if dataset not in df_inputs["ID"].values:
                    df_inputs.loc[len(df_inputs), "ID"] = dataset

            df_inputs = df_inputs[df_inputs["ID"].isin(list_datasets)]

            update_inputs_csv(
                df_inputs=df_inputs,
                working_path=working_path,
                study=col,
            )


def update_studies_settings(
    app: Application,
    dict_settings_wgt: dict,
    working_path: Path,
):
    for key, value in dict_settings_wgt.items():

        # -------------- #
        # Procs settings #
        # -------------- #
        dict_procs: dict = get_json_file(
            working_path=working_path,
            study=key,
            file_prefix="process",
        )
        for k, v in dict_procs.items():
            dict_procs[k]["execute"] = value["Procs"][k]["execute"].value
            dict_procs[k]["silent"] = value["Procs"][k]["silent"].value
        
        update_json_file(
            dict=dict_procs,
            working_path=working_path,
            study=key,
            file_prefix="process",
        )
        
        # ------------ #
        # Fixed inputs #
        # ------------ #
        dict_inputs = get_json_file(
            working_path=working_path,
            study=key,
            file_prefix="inputs",
        )

        # Fixed params
        for k, v in value["Fixed"]["params"].items():
            if (app.workflow.params_type[k][1] == "float") and (v.value is not None):
                dict_inputs[k] = float(v.value)
            else:
                dict_inputs[k] = v.value

        # Fixed paths
        for k, v in value["Fixed"]["paths"].items():
            if v.value.strip() != "":
                dict_inputs[k] = v.value
            else:
                dict_inputs[k] = None
        
        # --------------- #
        # Variable inputs #
        # --------------- #
        df_inputs = get_inputs_csv(
            app=app,
            working_path=working_path,
            study=key,
        )
        if df_inputs is not None:
            for dataset in df_inputs["ID"]:

                # execute
                df_inputs.loc[df_inputs["ID"] == dataset, "EXECUTE"] = int(value["Variable"][dataset]["execute"].value)

                # Variable params
                for k, v in value["Variable"][dataset]["params"].items():
                    if v.value is not None:
                        if (app.workflow.params_type[k][1] == "float"):
                            df_inputs.loc[df_inputs["ID"] == dataset, k] = float(v.value)
                        elif (app.workflow.params_type[k][1] == "int"):
                            df_inputs.loc[df_inputs["ID"] == dataset, k] = int(v.value)
                        elif (app.workflow.params_type[k][1] == "bool"):
                            df_inputs.loc[df_inputs["ID"] == dataset, k] = bool(v.value)
                        elif (app.workflow.params_type[k][1] == "str"):
                            df_inputs.loc[df_inputs["ID"] == dataset, k] = str(v.value)
                    else:
                        df_inputs.loc[df_inputs["ID"] == dataset, k] = v.value
                
                # Variable paths
                for k, v in value["Variable"][dataset]["paths"].items():
                    if v.value.strip() != "":
                        dict_inputs[k][dataset] = v.value
                    else:
                        dict_inputs[k][dataset] = None

            update_inputs_csv(
                df_inputs=df_inputs,
                working_path=working_path,
                study=key,
            )

        update_json_file(
            dict=dict_inputs,
            working_path=working_path,
            study=key,
            file_prefix="inputs",
        )