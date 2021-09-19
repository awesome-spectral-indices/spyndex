from typing import Any

import pandas as pd
import xarray as xr

from .utils import _load_JSON


def open(dataset: str) -> Any:
    """Opens a dataset.

    Parameters
    ----------
    dataset : str
        One of "sentinel" or "spectral". The sentinel dataset is loaded as a
        :code:`xarray.DataArray` with a sample image of the Sentinel-2 satellite
        (10 m bands). The spectral dataset is loaded as a :code:`pandas.DataFrame`
        with Landsat 8 reflectance samples of three different land covers.

    Returns
    -------
    Any
        Loaded dataset.

    Examples
    --------
    Open the :code:`sentinel` dataset:

    >>> import spyndex
    >>> spyndex.datasets.open("sentinel")
    <xarray.DataArray (band: 4, x: 300, y: 300)>
    Coordinates:
    * band     (band) <U3 'B02' 'B03' 'B04' 'B08'
    Dimensions without coordinates: x, y

    Open the :code:`spectral` dataset:
    
    >>> spt = spyndex.datasets.open("spectral")
    >>> spt.dtypes
    SR_B1     float64
    SR_B2     float64
    SR_B3     float64
    SR_B4     float64
    SR_B5     float64
    SR_B6     float64
    SR_B7     float64
    ST_B10    float64
    class      object
    dtype: object
    >>> spt.shape
    (120, 9)
    """

    datasets = {"sentinel": "S2_10m.json", "spectral": "spectral.json"}

    if dataset not in list(datasets.keys()):
        raise Exception(
            f"{dataset} is not a valid dataset. Please use one of ['sentinel','spectral']"
        )

    ds = _load_JSON(datasets[dataset])

    if dataset == "sentinel":
        ds = xr.DataArray(
            ds, dims=("band", "x", "y"), coords={"band": ["B02", "B03", "B04", "B08"]}
        )
    elif dataset == "spectral":
        ds = pd.DataFrame(ds)

    return ds
