import re
from typing import Any, List, Optional, Union

import dask
import dask.array as da
import dask.dataframe as dd
import ee
import eemont
import numpy as np
import pandas as pd
import xarray as xr

from .utils import _check_params, _get_indices


def computeIndex(
    index: Union[str, List[str]],
    params: dict,
    online: bool = False,
    returnOrigin: bool = True,
    coordinate: str = "index",
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
        object is returned. When dask objects are used, dask objects are returned.
        If false, a list is returned.
    coordinate : str, default = "index"
        Name of the coordinate used to concatenate DataArray objects when
        :code:`returnOrigin = True`.

    Returns
    -------
    Any
        Computed Spectral Indices according to the inputs' type.

    Examples
    --------
    Compute a Spectral Index by passing the required :code:`params` dictionary:

    >>> import spyndex
    >>> idx = spyndex.computeIndex(
    ...     index = "NDVI",
    ...     params = {
    ...         "N": 0.643,
    ...         "R": 0.175
    ...     }
    ... )
    0.5721271393643031

    Two or more Spectral Indices can be computed:

    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI"],
    ...     params = {
    ...         "N": 0.643,
    ...         "R": 0.175,
    ...         "L": 0.5
    ...     }
    ... )
    [0.5721271393643031, 0.5326251896813354]

    Spyndex is versatile. Let's compute Spectral Indices from a numpy array:

    >>> import numpy as np
    >>> R = np.random.normal(0.12,0.05,10000)
    >>> G = np.random.normal(0.34,0.07,10000)
    >>> N = np.random.normal(0.67,0.12,10000)
    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI","GNDVI"],
    ...     params = {
    ...         "N": N,
    ...         "R": R,
    ...         "G": G,
    ...         "L": 0.5
    ...     }
    ... )
    array([[0.57190873, 0.63776266, 0.52554653, ..., 0.692647  , 0.72013087,
            0.57576994],
           [0.5494994 , 0.60604837, 0.47157809, ..., 0.60647869, 0.65887439,
            0.52585032],
           [0.33304486, 0.46408771, 0.28007567, ..., 0.35734698, 0.28536337,
            0.50212151]])

    Now, let's try a pandas DataFrame:

    >>> import pandas as pd
    >>> df = pd.DataFrame({"Red":R,"Green":G,"NIR":N})
    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI","GNDVI"],
    ...     params = {
    ...         "N": df["NIR"],
    ...         "R": df["Red"],
    ...         "G": df["Green"],
    ...         "L": 0.5
    ...     }
    ... )
            NDVI      SAVI     GNDVI
    0     0.571909  0.549499  0.333045
    1     0.637763  0.606048  0.464088
    2     0.525547  0.471578  0.280076
    3     0.498328  0.443842  0.514775
    4     0.625445  0.512757  0.227829
    ...        ...       ...       ...
    9995  0.706123  0.604131  0.233519
    9996  0.731205  0.630090  0.389462
    9997  0.692647  0.606479  0.357347
    9998  0.720131  0.658874  0.285363
    9999  0.575770  0.525850  0.502122

    What about a xarray DataArray?

    >>> import xarray as xr
    >>> da = xr.DataArray(np.array([G,R,N]).reshape(3,100,100),
    ...     dims = ("band","x","y"),
    ...     coords = {"band": ["Green","Red","NIR"]})
    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI","GNDVI"],
    ...     params = {
    ...         "N": da.sel(band = "NIR"),
    ...         "R": da.sel(band = "Red"),
    ...         "G": da.sel(band = "Green"),
    ...         "L": 0.5
    ...     }
    ... )
    <xarray.DataArray (index: 3, x: 100, y: 100)>
    Coordinates:
        * index    (index) <U5 'NDVI' 'SAVI' 'GNDVI'
    Dimensions without coordinates: x, y
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
            _check_params(idx, params)
            result.append(eval(indices[idx]["formula"], params))

    if len(result) == 1:
        result = result[0]
    else:
        if returnOrigin:
            if isinstance(result[0], np.ndarray):
                result = np.array(result)
            elif isinstance(result[0], pd.core.series.Series):
                result = pd.DataFrame(dict(zip(index, result)))
            elif isinstance(result[0], xr.core.dataarray.DataArray):
                result = xr.concat(result, dim=coordinate).assign_coords(
                    {coordinate: index}
                )
            elif isinstance(result[0], ee.image.Image):
                result = ee.Image(result).rename(index)
            elif isinstance(result[0], dask.array.core.Array):
                result = da.array(result)

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
    Any
        Computed kernel.
    """

    kernels = {
        "linear": "a * b",
        "poly": "((a * b) + c) ** p",
    }

    if isinstance(params["a"], ee.image.Image) or isinstance(
        params["b"], ee.image.Image
    ):
        kernels["RBF"] = "exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))"
        result = params["a"].expression(kernels[kernel], params)
    else:
        kernels["RBF"] = "np.exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))"
        params["np"] = np
        result = eval(kernels[kernel], params)

    return result
