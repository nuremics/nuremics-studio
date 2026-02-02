from importlib.resources import files

import nuremics_studio.core.utils as utils


def get_app_features():
    
    app_features = {}

    app_features["import"] = "general.DEMO_APP"
    app_features["link"] = "https://nuremics.github.io/labs/apps/general/DEMO_APP"
    app_features["visual"] = "https://raw.githubusercontent.com/nuremics/nuremics-docs/main/docs/images/DEMO_APP.png"
    # app_features["logo"] = utils.image_to_data_url(files("nuremics_studio.resources").joinpath("logo.png"))
    # app_features["color"] = "#101a30"

    return app_features