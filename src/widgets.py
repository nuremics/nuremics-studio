import marimo as mo
import pandas as pd
from pathlib import Path

import utils
from nuremics import Application


def working_dir(
    working_dir: str,
):
    widget = mo.ui.text(
        label="Working directory:",
        value=working_dir,
    )

    return widget


def studies(
    list_studies: list[str],
):
    if list_studies:
        df = pd.DataFrame({"Studies": list_studies})
    else:
        df = pd.DataFrame({"Studies": pd.Series(dtype=str)})
    
    widget = mo.ui.data_editor(df)

    return widget


def config(
    dict_studies: dict,
    set_state,
):
    dict_widget = {}
    dict_tabs = {}
    for key, value in dict_studies["config"].items():

        list_wgt = []
        dict_widget[key] = {}

        execute_wgt = mo.ui.checkbox(
            label="execute",
            value=value["execute"],
            on_change=set_state,
        )
        list_wgt.append(mo.vstack([execute_wgt]))
        dict_widget[key]["execute"] = execute_wgt

        list_wgt.append(mo.md("**INPUT PARAMETERS** _(check parameters that are variable within the study)_"))

        dict_user_params_wgt = {}
        for k, v in value["user_params"].items():
            if v is None:
                val = False
            else:
                val = v
            w = mo.ui.checkbox(
                label=k,
                value=val,
                on_change=set_state,
            )
            dict_user_params_wgt[k] = w
            list_wgt.append(w)

        dict_widget[key]["user_params"] = dict_user_params_wgt

        list_wgt.append(mo.md("**INPUT PATHS** _(check paths that are variable within the study)_"))

        dict_user_paths_wgt = {}
        for k, v in value["user_paths"].items():
            if v is None:
                val = False
            else:
                val = v
            w = mo.ui.checkbox(
                label=k,
                value=val,
                on_change=set_state,
            )
            dict_user_paths_wgt[k] = w
            list_wgt.append(w)

        dict_widget[key]["user_paths"] = dict_user_paths_wgt

        tab = mo.vstack(list_wgt)
        dict_tabs[key] = tab

    widget = mo.ui.tabs(
        tabs=dict_tabs,
    )

    return widget, dict_widget


def settings(
    app: Application,
    working_path: Path,
    list_studies: list[str],
):
    dict_widget = {}
    dict_tabs = {}
    for study in list_studies:

        dict_widget[study] = {}

        # ------------ #
        # Fixed inputs #
        # ------------ #
        dict_tab = {
            "Fixed": {},
        }
        list_fixed_params_wgt = []
        list_fixed_paths_wgt = []

        dict_inputs: dict = utils.get_json_inputs(
            working_path=working_path,
            study=study,
        )

        # Fixed params
        list_fixed_params_wgt.append(mo.md("**INPUT PARAMETERS** _(set parameters values)_"))

        for k, v in dict_inputs.items():
            if k in app.workflow.params_type:

                if app.workflow.params_type[k][1] == "float":
                    w = mo.ui.number(
                        label=f"{k}:",
                        value=v,
                    )
                    list_fixed_params_wgt.append(w)

                if app.workflow.params_type[k][1] == "int":
                    w = mo.ui.number(
                        label=f"{k}:",
                        value=v,
                        step=1,
                    )
                    list_fixed_params_wgt.append(w)

                if app.workflow.params_type[k][1] == "bool":
                    if v is None:
                        val = False
                    else:
                        val = v
                    w = mo.ui.checkbox(
                        label=k,
                        value=val,
                    )
                    list_fixed_params_wgt.append(w)

                if app.workflow.params_type[k][1] == "str":
                    if v is None:
                        val = ""
                    else:
                        val = v
                    w = mo.ui.text(
                        label=f"{k}:",
                        value=val,
                    )
                    list_fixed_params_wgt.append(w)

        # Fixed paths
        list_fixed_paths_wgt.append(mo.md("**INPUT PATHS** _(set paths or add files/folders to the requested location)_"))

        for k, v in dict_inputs.items():
            if (k in app.workflow.user_paths) and (not isinstance(v, dict)):

                if v is None:
                    val = ""
                else:
                    val = v
                w = mo.ui.text(
                    label=f"{k}:",
                    value=val,
                )
                w = mo.hstack(
                    [w, mo.md(f"`{working_path / f'{study}/0_inputs'}`")],
                    justify="start",
                    align="center",
                )
                list_fixed_paths_wgt.append(w)

        dict_tab["Fixed"] = mo.vstack([
                mo.vstack([mo.md("    ")]),
                mo.vstack(list_fixed_params_wgt),
                mo.vstack([mo.md("    ")]),
                mo.vstack(list_fixed_paths_wgt),
            ],
        )

        # --------------- #
        # Variable inputs #
        # --------------- #
        df_inputs = utils.get_csv_inputs(
            app=app,
            working_path=working_path,
            study=study,
        )

        if df_inputs is not None:

            dict_tab["Variable"] = {}
            list_variable_params_wgt = []
            list_variable_paths_wgt = []
            
            # Variable params
            list_variable_params_wgt.append(mo.md("**INPUT DATASETS / PARAMETERS** _(define datasets and set parameters values)_"))
            
            w = mo.ui.data_editor(df_inputs)
            list_variable_params_wgt.append(w)

            # Variable paths
            list_variable_paths_wgt.append(mo.md("**INPUT PATHS** _(set paths or add files/folders to the requested location)_"))

            dict_tab["Variable"] = mo.vstack([
                    mo.vstack([mo.md("    ")]),
                    mo.vstack(list_variable_params_wgt),
                    mo.vstack([mo.md("    ")]),
                    mo.vstack(list_variable_paths_wgt),
                ],
            )

        dict_tabs[study] = mo.ui.tabs(
            tabs=dict_tab,
        )

    widget = mo.ui.tabs(
        tabs=dict_tabs,
    )

    return widget