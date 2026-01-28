import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import sys
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
    app_logo = app_features["logo"]
    app_color = app_features["color"]

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
    workflow, app = main(stage=None)

    dict_settings = utils.get_settings()

    if dict_settings["apps"][app_name]["working_dir"] is not None:
        working_dir = dict_settings["apps"][app_name]["working_dir"]
    else:
        if dict_settings["default_working_dir"] is not None:
            working_dir = dict_settings["default_working_dir"]
        else:
            working_dir = ""
    return app, dict_settings, working_dir


@app.cell(hide_code=True)
def _(working_dir):
    working_dir_wgt = wgt.working_dir(
        working_dir=working_dir,
    )
    working_dir_wgt
    return (working_dir_wgt,)


@app.cell(hide_code=True)
def _(working_dir_wgt):
    is_valid_working_dir = working_dir_wgt.value != ""
    return (is_valid_working_dir,)


@app.cell(hide_code=True)
def _(is_valid_working_dir):
    mo.stop(not is_valid_working_dir)

    mo.md(r"""
    ### Studies
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _(dict_settings, is_valid_working_dir, working_dir_wgt):
    mo.stop(not is_valid_working_dir)

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
    return (studies_wgt,)


@app.cell(hide_code=True)
def _(studies_wgt):
    list_studies = [
        s for s in studies_wgt.value["Studies"].tolist() if s != ""
    ]
    is_valid_list_studies = bool(list_studies)
    return is_valid_list_studies, list_studies


@app.cell(hide_code=True)
def _(is_valid_list_studies, list_studies, working_path):
    mo.stop(not is_valid_list_studies)

    utils.update_list_studies(
        working_path=working_path,
        list_studies=list_studies,
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
def _(dict_studies_to_config, is_valid_list_studies):
    mo.stop(not is_valid_list_studies)

    get_state_config, set_state_config = mo.state(0)

    config_wgt, dict_config_wgt = wgt.config(
        dict_studies=dict_studies_to_config,
        set_state=set_state_config,
    )
    config_wgt
    return dict_config_wgt, get_state_config


@app.cell(hide_code=True)
def _(
    dict_config_wgt,
    dict_studies_to_config,
    get_state_config,
    is_valid_list_studies,
    working_path,
):
    mo.stop(not is_valid_list_studies)

    _ = get_state_config()

    dict_studies_configured = utils.update_dict_studies(
        dict_studies=dict_studies_to_config,
        dict_config_wgt=dict_config_wgt,
    )

    utils.update_studies(
        working_path=working_path,
        dict_studies=dict_studies_configured,
    )

    try:
        _, app_configured = main(stage="config")
    except SystemExit:
        pass
    return (app_configured,)


@app.cell(hide_code=True)
def _(is_valid_list_studies):
    mo.stop(not is_valid_list_studies)

    mo.md(r"""
    ### Settings
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _(
    app_configured,
    get_state_config,
    is_valid_list_studies,
    list_studies,
    working_path,
):
    mo.stop(not is_valid_list_studies)

    _ = get_state_config()

    get_state_datasets, set_state_datasets = mo.state(0)

    datasets_wgt, dict_datasets_wgt = wgt.datasets(
        app=app_configured,
        working_path=working_path,
        list_studies=list_studies,
        set_state=set_state_datasets,
    )
    datasets_wgt
    return dict_datasets_wgt, get_state_datasets


@app.cell(hide_code=True)
def _(
    app,
    dict_datasets_wgt,
    get_state_datasets,
    is_valid_list_studies,
    working_path,
):
    mo.stop(not is_valid_list_studies)

    _ = get_state_datasets()

    utils.update_datasets(
        app=app,
        dict_datasets_wgt=dict_datasets_wgt,
        working_path=working_path,
    )
    return


@app.cell(hide_code=True)
def _(get_state_datasets, is_valid_list_studies):
    mo.stop(not is_valid_list_studies)

    _ = get_state_datasets()

    try:
        main(stage="settings")
    except SystemExit:
        pass
    return


@app.cell
def _(
    app_configured,
    get_state_config,
    get_state_datasets,
    is_valid_list_studies,
    list_studies,
    working_path,
):
    mo.stop(not is_valid_list_studies)

    _ = get_state_config()
    _ = get_state_datasets()

    get_state_settings, set_state_settings = mo.state(0)

    settings_wgt, dict_settings_wgt = wgt.settings(
        app=app_configured,
        working_path=working_path,
        list_studies=list_studies,
        set_state=set_state_settings,
    )
    settings_wgt
    return dict_settings_wgt, get_state_settings


@app.cell
def _(
    app,
    dict_settings_wgt,
    get_state_settings,
    is_valid_list_studies,
    working_path,
):
    mo.stop(not is_valid_list_studies)

    # print(dict_settings_wgt)

    _ = get_state_settings()

    utils.update_studies_settings(
        app=app,
        dict_settings_wgt=dict_settings_wgt,
        working_path=working_path,
    )
    return


@app.cell(disabled=True)
def _(pd):
    #import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})

    editor = mo.ui.data_editor(data=df, label="Edit Data")

    dict_tabs = {
        "tab1": editor,
        "tab2": "test"
    }

    tabs = mo.ui.tabs(
        tabs=dict_tabs,
    )

    tabs

    # acc = mo.accordion(
    #     {
    #         "Door 1": editor,
    #         "Door 2": mo.md("Nothing!"),
    #     }
    # )
    # acc
    return


@app.cell
def _(get_state_datasets, get_state_settings, is_valid_list_studies):
    mo.stop(not is_valid_list_studies)

    _ = get_state_settings()
    _ = get_state_datasets()

    try:
        main(stage="settings")
    except SystemExit:
        pass
    return


if __name__ == "__main__":
    app.run()
