import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import sys
    import copy
    import attrs
    import importlib
    import marimo as mo
    from pathlib import Path

    import utils
    import widgets as wgt

    app_name = sys.argv[1]

    app_features = utils.get_app_features(
        app_name=app_name,
    )
    app_import = app_features["import"]
    app_link = app_features["link"]
    app_visual = app_features["visual"]

    module_path = f"nuremics_labs.apps.{app_import}"
    module = importlib.import_module(module_path)
    main = getattr(module, "main")


@app.cell(hide_code=True)
def _():
    mo.Html(f"""
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

        background-color: #6eb6ffae;
        padding: 14px 20px;
        border-radius: 10px;

        box-shadow: 0 0 14px rgba(0, 0, 0, 0.25);

        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .jost-banner:hover {{
        transform: scale(1.005);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.25); /* ombre un peu plus marquée */
    }}

    .jost-banner img {{
        height: 50px;
    }}
    </style>

    <a href="{app_link}" target="_blank" class="jost-banner-link">
        <div class="jost-banner">
            <img src="https://raw.githubusercontent.com/nuremics/nuremics-docs/main/docs/images/logo.png">
            <div>
                <strong> {app_name} </strong>
            </div>
        </div>
    </a>
    """)
    return


@app.cell(hide_code=True)
def _():
    image = mo.image(
        src=app_visual,
        width=None,
    )
    mo.vstack([mo.vstack([image], align="center")])
    return


@app.cell(disabled=True)
def _():
    image2 = mo.image(
        src="https://splinecloud.com/img/sc-logo.png",
        width=None,
    )
    mo.vstack([mo.vstack([image2], align="center")])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Configuration
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _():
    workflow = main(stage=None)
    dict_settings = utils.get_settings()

    if dict_settings["apps"][app_name]["working_dir"] is not None:
        working_dir = dict_settings["apps"][app_name]["working_dir"]
    else:
        if dict_settings["default_working_dir"] is not None:
            working_dir = dict_settings["default_working_dir"]
        else:
            working_dir = ""
    return dict_settings, workflow, working_dir


@app.cell(hide_code=True)
def _(working_dir):
    working_dir_wgt = wgt.working_dir(
        working_dir=working_dir,
    )
    working_dir_wgt
    return (working_dir_wgt,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Studies
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _(dict_settings, working_dir_wgt):
    dict_settings["apps"][app_name]["working_dir"] = working_dir_wgt.value

    utils.update_settings(
        dict_settings=dict_settings,
    )

    working_path = Path(working_dir_wgt.value) / app_name

    try:
        main(stage="config")
    except SystemExit:
        pass
    return (working_path,)


@app.cell(hide_code=True)
def _(working_path):
    dict_studies_init = utils.get_studies(
        working_path=working_path,
    )

    studies_wgt = wgt.studies(
        list_studies=dict_studies_init["studies"],
    )
    studies_wgt
    return dict_studies_init, studies_wgt


@app.cell(hide_code=True)
def _(dict_studies_init, studies_wgt, working_path):
    list_studies = studies_wgt.value["Studies"].astype(str).tolist()
    dict_studies_init["studies"] = list_studies

    utils.update_studies(
        working_path=working_path,
        dict_studies=dict_studies_init,
    )

    try:
        main(stage="config")
    except SystemExit:
        pass

    dict_studies_to_config = utils.get_studies(
        working_path=working_path,
    )
    return (dict_studies_to_config,)


@app.cell(hide_code=True)
def _(dict_studies_to_config):
    get_state_config, set_state_config = mo.state(0)

    config_wgt, dict_config_wgt = wgt.config(
        dict_studies=dict_studies_to_config,
        set_state=set_state_config,
    )
    config_wgt
    return dict_config_wgt, get_state_config


@app.cell(hide_code=True)
def _(dict_config_wgt, dict_studies_to_config, get_state_config, working_path):
    _ = get_state_config()

    dict_studies_configured = copy.deepcopy(dict_studies_to_config)
    for key, value in dict_studies_to_config["config"].items():

        dict_studies_configured["config"][key]["execute"] = dict_config_wgt[key]["execute"].value

        for k, _ in value["user_params"].items():
            dict_studies_configured["config"][key]["user_params"][k] = dict_config_wgt[key]["user_params"][k].value
        for k, _ in value["user_paths"].items():
            dict_studies_configured["config"][key]["user_paths"][k] = dict_config_wgt[key]["user_paths"][k].value

    utils.update_studies(
        working_path=working_path,
        dict_studies=dict_studies_configured,
    )

    try:
        main(stage="config")
    except SystemExit:
        pass
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Settings
    -----------------------------
    """)
    return


@app.cell
def _():

    # for i in list_studies:

    # tabs = mo.ui.tabs(
    #     tabs={

    #         },
    #     )
    # tabs
    return


@app.cell(disabled=True)
def _(workflow):
    for proc in workflow:
        process = proc["process"]

        for field in attrs.fields(process):
            if field.metadata.get("input", False):
                print(f"{field.name}, {field.type}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
