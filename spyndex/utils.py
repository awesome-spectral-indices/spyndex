import requests
import pkg_resources
import os
import json

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
    spyndexDir = os.path.dirname(
        pkg_resources.resource_filename("spyndex", "spyndex.py")
    )
    dataPath = os.path.join(spyndexDir, "data/" + file)
    f = open(dataPath)
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
            "https://raw.githubusercontent.com/davemlz/awesome-ee-spectral-indices/main/output/spectral-indices-dict.json"
        ).json()
    else:
        indices = _load_JSON()

    return indices["SpectralIndices"]