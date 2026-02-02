import marimo as mo
import pandas as pd
from pathlib import Path

from nuremics import Application
import nuremics_studio.core.utils as utils


def app_banner(
    app_name: str,
    app_logo: str,
    app_color: str,
    app_link: str,
):
    if app_link is not None:

        widget = mo.Html(f"""
            <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">

            <style>
            .jost-banner-link {{
                text-decoration: none;
                display: block;
            }}

            .jost-banner {{
                display: flex;
                align-items: center;
                gap: 14px;

                font-family: 'Jost', sans-serif;
                color: white;
                font-size: 30px;
                font-weight: 600;

                background-color: {app_color};
                padding: 14px 20px;
                border-radius: 10px;

                box-shadow: 0 0 14px rgba(0, 0, 0, 0.25);

                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}

            .jost-banner:hover {{
                transform: scale(1.005);
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.25);
            }}

            .jost-banner img {{
                height: 50px;
            }}
            </style>

            <a href="{app_link}" target="_blank" class="jost-banner-link">
                <div class="jost-banner">
                    <img src="{app_logo}">
                    <div>
                        <strong> {app_name} </strong>
                    </div>
                </div>
            </a>
        """)
    
    else:

        widget = mo.Html(f"""
            <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">

            <style>
            .jost-banner-link {{
                text-decoration: none;
                display: block;
            }}

            .jost-banner {{
                display: flex;
                align-items: center;
                gap: 14px;

                font-family: 'Jost', sans-serif;
                color: white;
                font-size: 30px;
                font-weight: 600;

                background-color: {app_color};
                padding: 14px 20px;
                border-radius: 10px;

                box-shadow: 0 0 14px rgba(0, 0, 0, 0.25);

                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}

            .jost-banner img {{
                height: 50px;
            }}
            </style>

            <div class="jost-banner">
                <img src="{app_logo}">
                <div>
                    <strong> {app_name} </strong>
                </div>
            </div>
        """)

    return widget


def app_visual(
    file: str,
):
    if file is not None:
        image = mo.image(
            src=file,
            width=None,
        )
        widget = mo.vstack([mo.vstack([image], align="center")])
    else:
        widget = mo.vstack([
            mo.vstack(["      "]),
            mo.vstack(["      "]),
            mo.vstack(["      "]),
        ])
    
    return widget


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

        execute_wgt = mo.ui.switch(
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


def datasets(
    app: Application,
    working_path: Path,
    list_studies: list[str],
    set_state,
):
    df_datasets = pd.DataFrame()
    for study in list_studies:
        df_inputs = utils.get_inputs_csv(
            app=app,
            working_path=working_path,
            study=study,
        )
        if df_inputs is not None:
            df_datasets[study] = df_inputs["ID"].astype(str)
    
    df_datasets = df_datasets.fillna("")
    if df_datasets.shape[1] != 0:
        widget = mo.ui.data_editor(
            data=df_datasets,
            on_change=set_state,
        )
    else:
        widget = None
    
    dict_widget = {"datasets": widget}

    return widget, dict_widget


def settings(
    app: Application,
    working_path: Path,
    list_studies: list[str],
    set_state,
):
    dict_widget = {}
    dict_tabs = {}
    for study in list_studies:

        dict_widget[study] = {}
        dict_tab = {}

        # -------------- #
        # Procs settings #
        # -------------- #
        dict_widget[study]["Procs"] = {}
        dict_procs_wgt = {}

        dict_procs = utils.get_json_file(
            working_path=working_path,
            study=study,
            file_prefix="process",
        )
        for key, value in dict_procs.items():
            
            dict_widget[study]["Procs"][key] = {}
            list_procs_wgt = []

            execute_wgt = mo.ui.switch(
                label="execute",
                value=value["execute"],
                on_change=set_state,
            )
            dict_widget[study]["Procs"][key]["execute"] = execute_wgt
            list_procs_wgt.append(execute_wgt)

            silent_wgt = mo.ui.switch(
                label="silent mode",
                value=value["silent"],
                on_change=set_state,
            )
            dict_widget[study]["Procs"][key]["silent"] = silent_wgt
            list_procs_wgt.append(silent_wgt)

            dict_procs_wgt[key] = mo.vstack(list_procs_wgt)

        # ------------ #
        # Fixed inputs #
        # ------------ #
        dict_widget[study]["Fixed"] = {}
        dict_widget[study]["Fixed"]["params"] = {}
        dict_widget[study]["Fixed"]["paths"] = {}

        dict_inputs: dict = utils.get_json_file(
            working_path=working_path,
            study=study,
            file_prefix="inputs",
        )
        
        if app.workflow.fixed_params[study] or app.workflow.fixed_paths[study]:
            
            dict_tab["Fixed"] = {}
            list_fixed_params_wgt = []
            list_fixed_paths_wgt = []

            # Fixed params
            if app.workflow.fixed_params[study]:
                list_fixed_params_wgt.append(mo.md("**INPUT PARAMETERS** _(set parameters values)_"))

            for param in app.workflow.fixed_params[study]:

                if app.workflow.params_type[param][1] == "float":
                    w = mo.ui.number(
                        label=f"{param}:",
                        value=dict_inputs[param],
                        on_change=set_state,
                    )

                elif app.workflow.params_type[param][1] == "int":
                    w = mo.ui.number(
                        label=f"{param}:",
                        value=dict_inputs[param],
                        step=1,
                        on_change=set_state,
                    )

                elif app.workflow.params_type[param][1] == "bool":
                    if dict_inputs[param] is None:
                        val = False
                    else:
                        val = dict_inputs[param]
                    w = mo.ui.checkbox(
                        label=param,
                        value=val,
                        on_change=set_state,
                    )

                elif app.workflow.params_type[param][1] == "str":
                    if dict_inputs[param] is None:
                        val = ""
                    else:
                        val = dict_inputs[param]
                    w = mo.ui.text(
                        label=f"{param}:",
                        value=val,
                        on_change=set_state,
                    )
                
                dict_widget[study]["Fixed"]["params"][param] = w
                list_fixed_params_wgt.append(w)

            # Fixed paths
            if app.workflow.fixed_paths[study]:
                list_fixed_paths_wgt.append(mo.md("**INPUT PATHS** _(set paths or add files/folders to the requested location)_"))

            for path in app.workflow.fixed_paths[study]:
                
                if dict_inputs[path] is None:
                    val = ""
                else:
                    val = dict_inputs[path]

                w = mo.ui.text(
                    label=f"{path}:",
                    value=val,
                    on_change=set_state,
                )
                dict_widget[study]["Fixed"]["paths"][path] = w
                w = mo.hstack(
                    [w, mo.md(f"`{working_path / f'{study}/0_inputs'}`")],
                    justify="start",
                    align="center",
                )
                list_fixed_paths_wgt.append(w)

            list_fixed_wgt = []
            if list_fixed_params_wgt:
                list_fixed_wgt.append(mo.vstack([mo.md("    ")]))
                list_fixed_wgt.append(mo.vstack(list_fixed_params_wgt))
            if list_fixed_paths_wgt:
                list_fixed_wgt.append(mo.vstack([mo.md("    ")]))
                list_fixed_wgt.append(mo.vstack(list_fixed_paths_wgt))

            dict_tab["Fixed"] = mo.vstack(list_fixed_wgt)

        # --------------- #
        # Variable inputs #
        # --------------- #
        dict_widget[study]["Variable"] = {}

        df_inputs = utils.get_inputs_csv(
            app=app,
            working_path=working_path,
            study=study,
        )
        if df_inputs is not None:

            dict_tab["Variable"] = {}
            dict_accordion_datasets = {}

            for dataset in df_inputs["ID"]:

                dict_widget[study]["Variable"][dataset] = {}
                dict_widget[study]["Variable"][dataset]["params"] = {}
                dict_widget[study]["Variable"][dataset]["paths"] = {}

                list_variable_params_wgt = []
                list_variable_paths_wgt = []

                execute_wgt = mo.ui.switch(
                    label="execute",
                    value=bool(df_inputs.loc[df_inputs["ID"] == dataset, "EXECUTE"].values[0]),
                    on_change=set_state,
                )
                dict_widget[study]["Variable"][dataset]["execute"] = execute_wgt
            
                # Variable params
                if app.workflow.variable_params[study]:
                    list_variable_params_wgt.append(mo.md("**INPUT PARAMETERS** _(set parameters values)_"))

                for param in app.workflow.variable_params[study]:
                    
                    val_param = df_inputs.loc[df_inputs["ID"] == dataset, param].values[0]
                    if pd.isna(val_param):
                        val_param = None

                    if app.workflow.params_type[param][1] == "float":
                        if val_param is not None:
                            val_param = float(val_param)
                        w = mo.ui.number(
                            label=f"{param}:",
                            value=val_param,
                            on_change=set_state,
                        )

                    elif app.workflow.params_type[param][1] == "int":
                        if val_param is not None:
                            val_param = int(val_param)
                        w = mo.ui.number(
                            label=f"{param}:",
                            value=val_param,
                            step=1,
                            on_change=set_state,
                        )

                    elif app.workflow.params_type[param][1] == "bool":
                        if val_param is None:
                            val = False
                        else:
                            val = bool(val_param)
                        w = mo.ui.checkbox(
                            label=param,
                            value=val,
                            on_change=set_state,
                        )

                    elif app.workflow.params_type[param][1] == "str":
                        if val_param is None:
                            val = ""
                        else:
                            val = str(val_param)
                        w = mo.ui.text(
                            label=f"{param}:",
                            value=val,
                            on_change=set_state,
                        )
                    
                    dict_widget[study]["Variable"][dataset]["params"][param] = w
                    list_variable_params_wgt.append(w)

                # Variable paths
                if app.workflow.variable_paths[study]:
                    list_variable_paths_wgt.append(mo.md("**INPUT PATHS** _(set paths or add files/folders to the requested location)_"))

                for path in app.workflow.variable_paths[study]:
                    
                    if dict_inputs[path][dataset] is None:
                        val = ""
                    else:
                        val = dict_inputs[path][dataset]

                    w = mo.ui.text(
                        label=f"{path}:",
                        value=val,
                        on_change=set_state,
                    )
                    dict_widget[study]["Variable"][dataset]["paths"][path] = w
                    w = mo.hstack(
                        [w, mo.md(f"`{working_path / f'{study}/0_inputs/0_datasets/{dataset}'}`")],
                        justify="start",
                        align="center",
                    )
                    list_variable_paths_wgt.append(w)

                list_variable_wgt = []
                list_variable_wgt.append(mo.vstack([mo.md("    ")]))
                list_variable_wgt.append(mo.vstack([execute_wgt]))
                if list_variable_params_wgt:
                    list_variable_wgt.append(mo.vstack([mo.md("    ")]))
                    list_variable_wgt.append(mo.vstack(list_variable_params_wgt))
                if list_variable_paths_wgt:
                    list_variable_wgt.append(mo.vstack([mo.md("    ")]))
                    list_variable_wgt.append(mo.vstack(list_variable_paths_wgt))

                dict_accordion_datasets[dataset] = mo.vstack(list_variable_wgt)

            dict_tab["Variable"] = mo.vstack([
                    mo.accordion(
                        items=dict_accordion_datasets,
                    ),
                ])

        dict_tabs[study] = mo.vstack([
            mo.vstack([mo.accordion(items=dict_procs_wgt)]),
            mo.vstack([mo.ui.tabs(tabs=dict_tab)]),
        ])

    widget = mo.ui.tabs(
        tabs=dict_tabs,
    )

    return widget, dict_widget