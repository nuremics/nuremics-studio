import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import sys
    import io
    import importlib
    import pandas as pd
    import marimo as mo
    import utils
    from pathlib import Path

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
    main(stage=None)
    dict_settings = utils.get_settings()

    if dict_settings["apps"][app_name]["working_dir"] is not None:
        dir = dict_settings["apps"][app_name]["working_dir"]
    else:
        if dict_settings["default_working_dir"] is not None:
            dir = dict_settings["default_working_dir"]
        else:
            dir = ""
    return dict_settings, dir


@app.cell(hide_code=True)
def _(dir):
    working_dir_wgt = mo.ui.text(
        label="Working directory:",
        value=dir,
    )
    working_dir_wgt
    return (working_dir_wgt,)


@app.cell(hide_code=True)
def _(dict_settings, working_dir_wgt):
    dict_settings["apps"][app_name]["working_dir"] = working_dir_wgt.value
    utils.update_settings(
        dict_settings=dict_settings,
    )

    working_dir: Path = Path(working_dir_wgt.value) / app_name

    try:
        main(stage="config")
    except SystemExit:
        pass
    return (working_dir,)


@app.cell
def _(working_dir: Path):
    dict_studies = utils.get_studies(
        working_dir=working_dir,
    )

    if dict_studies["studies"]:
        df = pd.DataFrame({"Studies": dict_studies["studies"]})
    else:
        df = pd.DataFrame({"Studies": pd.Series(dtype=str)})

    editor = mo.ui.data_editor(df)
    editor
    return dict_studies, editor


@app.cell(hide_code=True)
def _(dict_studies, editor, working_dir: Path):
    dict_studies["studies"] = editor.value["Studies"].astype(str).tolist()
    utils.update_studies(
        working_dir=working_dir,
        dict_studies=dict_studies,
    )

    try:
        main(stage="config")
    except SystemExit:
        pass
    return


if __name__ == "__main__":
    app.run()
