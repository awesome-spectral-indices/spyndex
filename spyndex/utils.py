import json
import os
from importlib import import_module
from importlib.resources import files

import requests

import spyndex


def _load_JSON(file="spectral-indices-dict.json"):
    """Loads the specified JSON file from the data folder.

    Parameters
    ----------
    file : str
        File name.

    Returns
    -------
    object
        JSON file.
    """
    data_file = files("spyndex.data") / file
    with data_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def _get_indices(online=False):
    """Retrieves the JSON of indices.

    Parameters
    ----------
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub
        repository and not from the local copy.

    Returns
    -------
    dict
        Indices.
    """
    if online:
        indices = requests.get(
            "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/spectral-indices-dict.json"
        ).json()
    else:
        indices = _load_JSON()

    return indices["SpectralIndices"]


def _check_params(index: str, params: dict, indices: dict):
    """Checks if the parameters dictionary contains all required bands for the index
    computation.

    Parameters
    ----------
    index : str
        Index to check.
    params : dict
        Parameters dictionary to check.
    indices : dict
        Indices dictionary to check.

    Returns
    -------
    None
    """
    for band in indices[index]["bands"]:
        if band not in list(params.keys()):
            raise Exception(
                f"'{band}' is missing in the parameters for {index} computation!"
            )


def _import_optional_dependency(module: str, extra: str = None):
    """Import an optional dependency or explain which spyndex extra provides it."""
    if extra is None:
        extra = module.split(".")[0]

    try:
        return import_module(module)
    except ImportError as error:
        raise ImportError(
            f"{module} features require the optional dependency "
            f"'spyndex[{extra}]'.\n"
            f"Install it with:\n\n    pip install 'spyndex[{extra}]'"
        ) from error


def _has_ee_image(params: dict):
    """Checks if earthengine is installed and if params has an ee.Image.

    Parameters
    ----------
    params : dict
        Dictionary to check.

    Returns
    -------
    None
    """
    try:
        import ee
        return any(isinstance(v, ee.Image) for v in params.values())
    except ImportError:
        return False


def _has_ee_number(params: dict):
    """Checks if earthengine is installed and if params has an ee.Number.

    Parameters
    ----------
    params : dict
        Dictionary to check.

    Returns
    -------
    None
    """
    try:
        import ee
        return any(isinstance(v, ee.Number) for v in params.values())
    except ImportError:
        return False


def _maybe_import_earthengine(params: dict):
    """Import Earth Engine and eemont if any param is an Earth Engine object, or raise if missing.

    Parameters
    ----------
    params : dict
        Dictionary to check.

    Returns
    -------
    None
    """
    try:
        import ee
    except ImportError:
        needs_ee = False
        for v in params.values():
            if v.__class__.__name__ in ("Image", "Number"):
                needs_ee = True
                break
        if needs_ee:
            raise ImportError(
                "Earth Engine features require the optional dependency 'spyndex[ee]'.\n"
                "Install it with:\n\n    pip install 'spyndex[ee]'"
            )
        else:
            return

    if any(isinstance(v, (ee.Image, ee.Number)) for v in params.values()):
        try:
            import eemont
        except ImportError:
            raise ImportError(
                "Earth Engine features also require 'eemont'.\n"
                "Install it with:\n\n    pip install 'spyndex[ee]'"
            )
