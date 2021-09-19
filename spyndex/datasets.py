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
    array([[[ 299,  276,  280, ...,  510,  516,  521],
            [ 287,  285,  284, ...,  503,  476,  469],
            [ 287,  292,  288, ...,  454,  411,  337],
            ...,
            [ 502,  508,  520, ...,  683,  670,  791],
            [ 486,  518,  532, ...,  688,  696,  693],
            [ 486,  506,  515, ...,  659,  671,  664]],

        [[ 469,  446,  466, ...,  695,  711,  728],
            [ 469,  437,  469, ...,  683,  694,  666],
            [ 460,  460,  460, ...,  628,  595,  527],
            ...,
            [ 804,  808,  832, ...,  920,  872, 1023],
            [ 787,  803,  822, ...,  890,  882,  871],
            [ 787,  799,  822, ...,  893,  832,  834]],

        [[ 319,  293,  328, ..., 1054, 1090, 1110],
            [ 327,  318,  345, ..., 1044, 1004,  952],
            [ 339,  355,  323, ...,  922,  784,  652],
            ...,
            [1528, 1516, 1516, ..., 1250, 1246, 1420],
            [1470, 1502, 1498, ..., 1316, 1200, 1162],
            [1394, 1480, 1472, ..., 1288, 1144, 1122]],
        ...
            [1836, 1874, 1916, ..., 2075, 1792, 1747],
            [1778, 1844, 1870, ..., 2087, 1830, 1675]]])
    Coordinates:
    * band     (band) <U3 'B02' 'B03' 'B04' 'B08'
    Dimensions without coordinates: x, y

    Open the :code:`spectral` dataset:
    >>> import spyndex
    >>> spyndex.datasets.open("spectral")
            SR_B1     SR_B2     SR_B3     SR_B4     SR_B5     SR_B6     SR_B7  \
    0    0.089850  0.100795  0.132227  0.165764  0.269054  0.306206  0.251949   
    1    0.073859  0.086990  0.124404  0.160979  0.281264  0.267596  0.217917   
    2    0.072938  0.086028  0.120994  0.140203  0.284220  0.258384  0.200098   
    3    0.087733  0.103916  0.135981  0.163976  0.254479  0.259580  0.216735   
    4    0.090593  0.109306  0.150350  0.181260  0.269535  0.273234  0.219554   
    ..        ...       ...       ...       ...       ...       ...       ...   
    115  0.018048  0.021540  0.040927  0.034438  0.287822  0.113253  0.053742   
    116  0.015325  0.019203  0.044750  0.029900  0.281608  0.101510  0.048325   
    117  0.014830  0.018460  0.035785  0.026242  0.239615  0.088942  0.040845   
    118  0.013620  0.017497  0.032512  0.028030  0.167703  0.071013  0.033997   
    119  0.014610  0.019588  0.033282  0.025583  0.194240  0.073927  0.033255   
    ...
            ST_B10       class  
    0    297.328396       Urban  
    1    297.107934       Urban  
    2    297.436064       Urban  
    3    297.203638       Urban  
    4    297.097680       Urban  
    ..          ...         ...  
    115  289.624179  Vegetation  
    116  289.108058  Vegetation  
    117  288.974755  Vegetation  
    118  289.596835  Vegetation  
    119  289.374663  Vegetation
    ...
    [120 rows x 9 columns]
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
