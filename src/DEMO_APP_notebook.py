import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import os
    import json
    import marimo as mo
    import pandas as pd
    from pathlib import Path
    from typing import Callable, Any

    from nuremics import Process
    from nuremics_labs.ops.general import polygon_geometry
    from nuremics_labs.ops.general import projectile_model
    from nuremics_labs.ops.general import trajectory_analysis

    # ------- #
    # General #
    # ------- #

    # Hard-coded variables
    APP_NAME = "DEMO_APP"
    PROC1_NAME = "PolygonGeometryProc"
    PROC2_NAME = "ProjectileModelProc"

    # Widgets
    working_dir_wgt = mo.ui.text(
        label="Working directory:",
        value="C:/Users/julie/nrs_working_dir",
    )
    study_wgt = mo.ui.text(
        label="Study:",
        value="Study_Shape",
    )
    datasetID_wgt = mo.ui.text(
        label="Dataset ID:",
        value="Test1",
    )
    silent_wgt = mo.ui.checkbox(
        label="silent mode",
        value=False,
    )

    # ------------------- #
    # PolygonGeometryProc #
    # ------------------- #

    # Hard-coded variables
    radius: float = 0.5
    coords_file: str = "points_coordinates.csv"
    fig_file1: str = "polygon_shape.png"

    # Widgets
    nb_sides_wgt = mo.ui.number(
        label="nb_sides:",
        value=3,
        step=1,
        start=3,
    )
    plot_title_wgt = mo.ui.text(
        label="plot_title:",
        value="2D polygon shape",
    )
    nb_sides_status_wgt = mo.ui.checkbox(
        value=False,
    )
    plot_title_status_wgt = mo.ui.checkbox(
        value=False,
    )

    # ------------------- #
    # ProjectileModelProc #
    # ------------------- #

    # Hard-coded variables
    results_file: str = "results.xlsx"
    fig_file2: str = "model_vs_theory.png"
    comp_folder: str = "comparison"

    # Widgets
    gravity_wgt = mo.ui.number(
        label="gravity:",
        value=-9.81,
        step=0.01,
    )
    mass_wgt = mo.ui.number(
        label="mass:",
        value=0.05,
        step=0.01,
    )
    v0_wgt = mo.ui.number(
        label="v0:",
        value=15.0,
        step=1.0,
    )
    angle_wgt = mo.ui.number(
        label="angle:",
        value=45.0,
        step=1.0,
    )
    timestep_wgt = mo.ui.number(
        label="timestep:",
        value=0.01,
        step=0.01,
    )
    fps_wgt = mo.ui.number(
        label="fps:",
        value=60,
        step=1,
    )
    window_size_wgt = mo.ui.number(
        label="window_size:",
        value=700,
        step=50,
    )
    gravity_status_wgt = mo.ui.checkbox(
        value=False,
    )
    mass_status_wgt = mo.ui.checkbox(
        value=False,
    )
    v0_status_wgt = mo.ui.checkbox(
        value=False,
    )
    angle_status_wgt = mo.ui.checkbox(
        value=False,
    )
    timestep_status_wgt = mo.ui.checkbox(
        value=False,
    )
    fps_status_wgt = mo.ui.checkbox(
        value=False,
    )
    window_size_status_wgt = mo.ui.checkbox(
        value=False,
    )

    # ---------- #
    # Run button #
    # ---------- #
    button = mo.ui.run_button()


@app.cell(hide_code=True)
def _():
    mo.vstack([mo.md(f"# {APP_NAME} _(notebook)_")], align="center")
    return


@app.cell(hide_code=True)
def _():
    mo.md(f"""
    ## Configuration
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            # mo.md("## Configuration"),
            mo.vstack([working_dir_wgt]),
            mo.hstack([study_wgt]),
            mo.hstack([datasetID_wgt]),
            mo.hstack([silent_wgt]),
            mo.md("-----------------------------"),
            mo.md("_(Check inputs that are variable within the study)_"),
            mo.hstack([nb_sides_status_wgt, nb_sides_wgt], align="center", justify="start"),
            mo.hstack([plot_title_status_wgt, plot_title_wgt], align="center", justify="start"),
            mo.hstack([gravity_status_wgt, gravity_wgt], align="center", justify="start"),
            mo.hstack([mass_status_wgt, mass_wgt], align="center", justify="start"),
            mo.hstack([v0_status_wgt, v0_wgt], align="center", justify="start"),
            mo.hstack([angle_status_wgt, angle_wgt], align="center", justify="start"),
            mo.hstack([timestep_status_wgt, timestep_wgt], align="center", justify="start"),
            mo.hstack([fps_status_wgt, fps_wgt], align="center", justify="start"),
            mo.hstack([window_size_status_wgt, window_size_wgt], align="center", justify="start"),
            mo.md("-----------------------------"),
            mo.vstack([button], align="center"),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.stop(not button.value)

    working_dir = Path(working_dir_wgt.value) / f"{APP_NAME}_notebook"
    working_dir.mkdir(
        exist_ok=True,
        parents=True,
    )

    study_dir = working_dir / study_wgt.value
    study_dir.mkdir(
        exist_ok=True,
        parents=True,
    )
    proc1_dir: Path = study_dir / f"1_{PROC1_NAME}"
    proc1_dir.mkdir(
        exist_ok=True,
        parents=True,
    )
    proc2_dir: Path = study_dir / f"2_{PROC2_NAME}"
    proc2_dir.mkdir(
        exist_ok=True,
        parents=True,
    )

    if nb_sides_status_wgt.value \
    or plot_title_status_wgt.value:
        variable_status1 = True
    else:
        variable_status1 = False

    if gravity_status_wgt.value \
    or mass_status_wgt.value \
    or v0_status_wgt.value \
    or angle_status_wgt.value \
    or timestep_status_wgt.value \
    or fps_status_wgt.value \
    or window_size_status_wgt.value:
        variable_status2 = True
    else:
        variable_status2 = False
    return proc1_dir, proc2_dir, study_dir, variable_status1, variable_status2


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Results
    -----------------------------
    """)
    return


@app.cell(hide_code=True)
def _(study_dir):
    mo.stop(not button.value)
    mo.vstack([mo.ui.file_browser(initial_path=study_dir)])
    return


@app.cell(hide_code=True)
def _(proc1_dir: Path, variable_status1):
    mo.stop(not button.value)

    if variable_status1:
        dataset_proc1_dir = proc1_dir / datasetID_wgt.value
        dataset_proc1_dir.mkdir(
            exist_ok=True,
            parents=True,
        )
    else:
        dataset_proc1_dir = proc1_dir

    os.chdir(dataset_proc1_dir)
    return


@app.cell(hide_code=True)
def polygon_geometry_proc():
    mo.stop(not button.value)

    df_points = polygon_geometry.generate_polygon_shape(
        radius=radius,
        n_sides=nb_sides_wgt.value,
        filename=coords_file,
    )
    df1 = pd.read_csv(coords_file, usecols=["X", "Y"])

    polygon_geometry.plot_polygon_shape(
        df_points=df_points,
        title=plot_title_wgt.value,
        filename=fig_file1,
        silent=True,
    )
    image1 = mo.image(
        src=fig_file1,
        width=600,
    )
    return df1, df_points, image1


@app.cell(hide_code=True)
def _(proc2_dir: Path, variable_status1, variable_status2):
    mo.stop(not button.value)

    if variable_status1 or variable_status2:
        dataset_proc2_dir = proc2_dir / datasetID_wgt.value
        dataset_proc2_dir.mkdir(
            exist_ok=True,
            parents=True,
        )
    else:
        dataset_proc2_dir = proc2_dir

    os.chdir(dataset_proc2_dir)
    return


@app.cell(hide_code=True)
def projectile_model_proc(df_points):
    mo.stop(not button.value)

    df_trajectory_model = projectile_model.simulate_projectile_motion(
        df_points=df_points,
        mass=mass_wgt.value,
        gravity=gravity_wgt.value,
        v0=v0_wgt.value,
        angle=angle_wgt.value,
        timestep=timestep_wgt.value,
        fps=fps_wgt.value,
        window_size=window_size_wgt.value,
        silent=silent_wgt.value,
    )

    df_trajectory_model_vs_theory = (
        projectile_model.calculate_analytical_trajectory(
            df=df_trajectory_model,
            v0=v0_wgt.value,
            angle=angle_wgt.value,
            gravity=gravity_wgt.value,
            filename=results_file,
        )
    )
    df2 = pd.read_excel(results_file)

    projectile_model.compare_model_vs_analytical_trajectories(
        df=df_trajectory_model_vs_theory,
        filename=fig_file2,
        silent=True,
    )

    image2 = mo.image(
        src=fig_file2,
        width=600,
    )
    return df2, image2


@app.cell(hide_code=True)
def _(df1, df2, image1, image2):
    tabs = mo.ui.tabs(
        {
            coords_file: mo.ui.table(df1, show_download=False),
            fig_file1: mo.vstack([mo.vstack([image1], align="center")]),
            results_file: mo.ui.table(df2),
            fig_file2: mo.vstack([mo.vstack([image2], align="center")]),
        }
    )
    tabs
    return


if __name__ == "__main__":
    app.run()
