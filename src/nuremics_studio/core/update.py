import copy
from pathlib import Path

from nuremics import Application
import nuremics_studio.core.utils as utils


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


def update_datasets(
    app: Application,
    dict_datasets_wgt: dict,
    working_path: Path,
):
    datasets = dict_datasets_wgt["datasets"]
    if datasets is not None:
        for col in datasets.value.columns:
            
            df_inputs = utils.get_inputs_csv(
                app=app,
                working_path=working_path,
                study=col,
            )
            
            list_datasets = [x for x in datasets.value[col].to_list() if x]
            for dataset in list_datasets:
                if dataset not in df_inputs["ID"].values:
                    df_inputs.loc[len(df_inputs), "ID"] = dataset

            df_inputs = df_inputs[df_inputs["ID"].isin(list_datasets)]

            utils.update_inputs_csv(
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
        dict_procs: dict = utils.get_json_file(
            working_path=working_path,
            study=key,
            file_prefix="process",
        )
        for k, v in dict_procs.items():
            dict_procs[k]["execute"] = value["Procs"][k]["execute"].value
            dict_procs[k]["silent"] = value["Procs"][k]["silent"].value
        
        utils.update_json_file(
            dict=dict_procs,
            working_path=working_path,
            study=key,
            file_prefix="process",
        )
        
        # ------------ #
        # Fixed inputs #
        # ------------ #
        dict_inputs = utils.get_json_file(
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
        df_inputs = utils.get_inputs_csv(
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

            utils.update_inputs_csv(
                df_inputs=df_inputs,
                working_path=working_path,
                study=key,
            )

        utils.update_json_file(
            dict=dict_inputs,
            working_path=working_path,
            study=key,
            file_prefix="inputs",
        )