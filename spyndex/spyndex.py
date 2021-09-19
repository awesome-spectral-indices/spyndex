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
        Index or list of indices to compute. Check all available indices from the
        `Awesome Spectral Indices Repository <https://github.com/davemlz/awesome-spectral-indices>`_.
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
            - :code:`pandas.Series`: Returns a :code:`pandas.DataFrame`.
            - :code:`numpy.ndarray`: Returns a :code:`numpy.ndarray`.
            - :code:`xarray.DataArray`: Returns a :code:`xarray.DataArray`.
            - :code:`ee.Image`: Returns a :code:`ee.Image`.
            - :code:`ee.Number`: Returns a :code:`ee.List`.
            - :code:`dask.Array`: Returns a :code:`dask.Array`.
            - :code:`dask.Series`: Returns a :code:`dask.DataFrame`.
        When numeric objects are used in combination with other objects, the type of the 
        other object is returned. If false, a list is returned.
    coordinate : str, default = "index"
        Name of the coordinate used to concatenate :code:`xarray.DataArray` objects when
        :code:`returnOrigin = True`.

    Returns
    -------
    Any
        Computed Spectral Indices according to the inputs' type.

    See Also
    --------
    computeKernel : Computes a kernel :code:`k(a,b)`.

    Examples
    --------
    Compute a Spectral Index by passing the required :code:`params` dictionary:

    >>> import spyndex
    >>> spyndex.computeIndex(
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

    Spyndex is versatile! Let's compute Spectral Indices from a :code:`numpy.ndarray`:

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

    Now, let's try a :code:`pandas.DataFrame`:

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

    What about a :code:`xarray.DataArray`?

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

    Now let's try :code:`dask`!

    >>> import dask.array as da
    >>> array_shape = (10000,10000)
    >>> chunk_size = (1000,1000)
    >>> dask_array = da.array([
    ...     da.random.normal(0.6,0.10,array_shape,chunks = chunk_size),
    ...     da.random.normal(0.1,0.05,array_shape,chunks = chunk_size),
    ...     da.random.normal(0.3,0.02,array_shape,chunks = chunk_size)
    ... ])
    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI","GNDVI"],
    ...     params = {
    ...         "N": dask_array[0],
    ...         "R": dask_array[1],
    ...         "G": dask_array[2],
    ...         "L": 0.5
    ...     }
    ... ).compute()

    And a :code:`dask.DataFrame`?

    >>> import dask.dataframe as dd
    >>> df = pd.DataFrame({
    ...     "NIR": np.random.normal(0.6,0.10,1000),
    ...     "RED": np.random.normal(0.1,0.05,1000),
    ...     "GREEN": np.random.normal(0.3,0.02,1000),
    ... })
    >>> df = dd.from_pandas(df,npartitions = 10)
    >>> spyndex.computeIndex(
    ...     index = ["NDVI","SAVI","GNDVI"],
    ...     params = {
    ...         "N": df["NIR"],
    ...         "R": df["RED"],
    ...         "G": df["GREEN"],
    ...         "L": 0.5
    ...     }
    ... ).compute()
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
            elif isinstance(result[0], ee.ee_number.Number):
                result = ee.List(result)
            elif isinstance(result[0], dask.array.core.Array):
                result = da.array(result)
            elif isinstance(result[0], dask.dataframe.core.Series):
                result = dd.concat(result, axis="columns")
                result.columns = index

    return result


def computeKernel(kernel: str, params: dict) -> Any:
    """Computes a kernel :code:`k(a,b)`.

    Kernel parameters are used for kernel indices like the kNDVI that requires the
    :code:`kNN` (:code:`k(N,N)`) and :code:`kNR` (:code:`k(N,R)`) parameters.

    Parameters
    ----------
    kernel : str
        Kernel to use. One of 'linear', 'poly' or 'RBF'.
    params : dict
        Parameters to use for the kernel computation.
        For :code:`kernel = 'linear'`, the parameters 'a' (band A) and 'b' (band B) must 
        be declared. For :code:`kernel = 'RBF'`, the parameters 'a' (band A), 'b' (band B) 
        and 'sigma' (length-scale) must be declared. For :code:`kernel = 'poly'`, the 
        parameters 'a' (band A), 'b' (band B), 'p' (kernel degree) and 'c' (trade-off) 
        must be declared.

    Returns
    -------
    Any
        Computed kernel.

    See Also
    --------
    computeIndex : Computes one or more Spectral Indices from the Awesome Spectral Indices 
        list.

    Examples
    --------
    Compute a kernel index with the help of :code:`spyndex.computeKernel()`:

    >>> import spyndex
    >>> spyndex.computeIndex(
    ...     index = "kNDVI",
    ...     params = {
    ...         "kNN": 1.0,
    ...         "kNR": spyndex.computeKernel(
    ...             kernel = "RBF",
    ...             params = {
    ...                 "a" : 0.68, "b": 0.13, "sigma": (0.68 + 0.13) / 2
    ...             }
    ...         )
    ...     }
    ... )
    0.4309459271768674

    Use the polynomial kernel:

    >>> import spyndex
    >>> spyndex.computeIndex(
    ...     index = "kNDVI",
    ...     params = {
    ...         "kNN": spyndex.computeKernel(
    ...             kernel = "poly",
    ...             params = {
    ...                 "a" : 0.68,
    ...                 "b": 0.68, 
    ...                 "p": 2.0,
    ...                 "c": spyndex.constants.c.default
    ...             }
    ...         ),
    ...         "kNR": spyndex.computeKernel(
    ...             kernel = "poly",
    ...             params = {
    ...                 "a" : 0.68,
    ...                 "b": 0.13, 
    ...                 "p": 2.0,
    ...                 "c": spyndex.constants.c.default
    ...             }
    ...         )
    ...     }
    ... )
    0.2870700138954041

    Now let's try a :code:`numpy.ndarray`:

    >>> import numpy as np
    >>> R = np.random.normal(0.12,0.05,10000)
    >>> N = np.random.normal(0.67,0.12,10000)
    >>> spyndex.computeIndex(
    ...     index = "kNDVI",
    ...     params = {
    ...         "kNN": 1.0,
    ...         "kNR": spyndex.computeKernel(
    ...             kernel = "RBF",
    ...             params = {
    ...                 "a" : N,
    ...                 "b" : R,
    ...                 "sigma" : np.mean([N,R],0)
    ...            }           
    ...         )
    ...     }
    ... )
    array([0.36776416, 0.57727362, 0.5252302 , ..., 0.5209451 , 0.53162097,
       0.67689597])

    It's time for a :code:`pandas.DataFrame`!

    >>> import pandas as pd
    >>> R = np.random.normal(0.12,0.05,10000)
    >>> N = np.random.normal(0.67,0.12,10000)
    >>> df = pd.DataFrame({"Red":R,"NIR":N})
    >>> spyndex.computeIndex(
    ...     index = "kNDVI",
    ...     params = {
    ...         "kNN": 1.0,
    ...         "kNR": spyndex.computeKernel(
    ...             kernel = "RBF",
    ...             params = {
    ...                 "a" : df["NIR"],
    ...                 "b" : df["Red"],
    ...                 "sigma" : df.mean(1)
    ...            }           
    ...         )
    ...     }
    ... )
    0       0.468294
    1       0.535752
    2       0.745249
    3       0.402761
    4       0.432528
            ...   
    9995    0.475168
    9996    0.482034
    9997    0.403363
    9998    0.489537
    9999    0.508163
    Length: 10000, dtype: float64
    """

    kernels = {
        "linear": "a * b",
        "poly": "((a * b) + c) ** p",
    }

    if (
        isinstance(params["a"], ee.image.Image)
        or isinstance(params["b"], ee.image.Image)
        or isinstance(params["a"], ee.ee_number.Number)
        or isinstance(params["b"], ee.ee_number.Number)
    ):
        kernels["RBF"] = "exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))"
        result = params["a"].expression(kernels[kernel], params)
    else:
        kernels["RBF"] = "np.exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))"
        params["np"] = np
        result = eval(kernels[kernel], params)

    return result
