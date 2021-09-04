import json
import os
import re
from typing import Any, List, Optional, Union

import ee
import numpy as np
import pandas as pd
import pkg_resources
import requests
import xarray as xr
from box import Box


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
        spyndexDir = os.path.dirname(
            pkg_resources.resource_filename("spyndex", "spyndex.py")
        )
        dataPath = os.path.join(spyndexDir, "data/spectral-indices-dict.json")
        f = open(dataPath)
        indices = json.load(f)

    return indices["SpectralIndices"]


def computeIndex(
    index: Union[str, List[str]],
    params: dict,
    online: bool = False,
    returnOrigin: bool = True,
    coordinate: str = "channel",
) -> Any:
    """Computes one or more Spectral Indices from the Awesome Spectral Indices list.

    Parameters
    ----------
    index : str | list[str]
        Index or list of indices to compute.
    params: dict
        Parameters used as inputs for the computation. The input data must be compatible
        with Overloaded Operators. Some inputs' types supported are pandas series,
        numpy arrays, xarray objects and numeric objects. Earth Engine objects are also
        compatible when using eemont.
    online : bool, default = False
        Whether to retrieve the most recent list of indices directly from the GitHub
        repository and not from the local copy.
    returnOrigin : bool, default = True
        Whether to return multiple indices as an object with the same type as the inputs.
        When pandas series are used, a pandas DataFrame is returned. When numpy arrays
        are used, a numpy array is returned. When xarray DataArrays are used, a xarray
        DataArray is returned. When Earth Engine Images are used, an Earth Engine Image
        is returned. When numeric objects are used, numeric objects are returned. When
        numeric objects are used in combination with other objects, the type of the other
        object is returned. If false, a list is returned.
    coordinate : str, default = "channel"
        Name of the coordinate used to concatenate DataArray objects when
        :code:`returnOrigin = True`.

    Returns
    -------
    object
        Computed Spectral Indices according to the inputs' type.
    """

    if not isinstance(index, list):
        index = [index]

    indices = _get_indices(online)
    names = list(indices.keys())

    result = []
    for idx in index:
        if idx not in names:
            raise Exception(f"{idx} is not a valid Spectral Index!")
        else:
            result.append(eval(indices[idx]["formula"], params))

    if len(result) == 1:
        result = result[0]
    else:
        if returnOrigin:
            if isinstance(result[0], np.ndarray):                
                result = np.array(result)
            elif isinstance(result[0], pd.core.series.Series):
                result = pd.DataFrame(dict(zip(index,result)))
            elif isinstance(result[0], xr.core.dataarray.DataArray):                
                result = xr.concat(result, dim=coordinate).assign_coords(
                    {coordinate=(coordinate,index)}
                )
            elif isinstance(result[0], ee.image.Image):                
                result = ee.Image(result).rename(index)

    return result


def computeKernel(kernel: str, params: dict) -> Any:
    """Computes a kernel :code:`k(a,b)` to use for Kernel Indices computation.

    Parameters
    ----------
    kernel : str
        Kernel to use. One of 'linear', 'poly' or 'RBF'.
    params : dict
        Parameters to use for the kernel computation.
        For kernel = 'linear', the parameters 'a' (band A) and 'b' (band B) must be 
        declared. For kernel = 'RBF', the parameters 'a' (band A), 'b' (band B) and 
        'sigma' (length-scale) must be declared. For kernel = 'poly', the parameters 'a' 
        (band A), 'b' (band B), 'p' (kernel degree) and 'c' (trade-off) must be declared.

    Returns
    -------
    object
        Computed kernel.
    """

    kernels = {
        "linear": "a * b",
        "RBF": "np.exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))",
        "poly": "((a * b) + c) ** p",
    }

    params["np"] = np

    return eval(kernels[kernel], params)
