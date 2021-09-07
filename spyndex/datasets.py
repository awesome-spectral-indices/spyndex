from typing import Any

import xarray as xr

from .utils import _load_JSON


def open(dataset: str) -> Any:
    """Open a dataset.

    Parameters
    ----------
    dataset : str
        One of "sentinel" or "spectral". The sentinel dataset is loaded as a
        xarray.DataArray with a sample image of the Sentinel-2 satellite (10 m bands).

    Returns
    -------
    object
        Loaded dataset.

    Examples
    --------
    >>> import spyndex
    >>> snt = spyndex.datasets.open("sentinel")
    """

    datasets = {"sentinel": "S2_10m.json"}

    if dataset not in list(datasets.keys()):
        raise Exception(
            f"{dataset} is not a valid dataset. Please use one of ['sentinel']"
        )

    ds = _load_JSON(datasets[dataset])

    if dataset == "sentinel":
        ds = xr.DataArray(
            ds, dims=("band", "x", "y"), coords={"band": ["B02", "B03", "B04", "B08"]}
        )

    return ds
