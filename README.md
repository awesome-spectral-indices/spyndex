<p align="center">
  <a href="https://github.com/davemlz/spyndex"><img src="https://raw.githubusercontent.com/davemlz/spyndex/main/docs/_static/spyndex.png" alt="spyndex"></a>
</p>
<p align="center">
    <em><a href="https://github.com/davemlz/awesome-ee-spectral-indices" target="_blank">
    Awesome Spectral Indices</a> in Python:</em>
</p>
<p align="center">
    <b><a href="https://github.com/numpy/numpy" target="_blank">
    Numpy</a> | <a href="https://github.com/pandas-dev/pandas" target="_blank">
    Pandas</a> | <a href="https://github.com/pydata/xarray" target="_blank">
    Xarray</a> | <a href="https://github.com/google/earthengine-api" target="_blank">
    Earth Engine</a> | <a href="https://github.com/microsoft/planetary-computer-sdk-for-python" target="_blank">
    Planetary Computer</a> </b>
</p>
<p align="center">
<a href="https://github.com/davemlz/spyndex/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/davemlz/spyndex/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://github.com/davemlz/spyndex/actions/workflows/update_awesome_spectral_indices.yml" target="_blank">
    <img src="https://github.com/davemlz/spyndex/actions/workflows/update_awesome_spectral_indices.yml/badge.svg" alt="Awesome Spectral Indices">
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href="https://github.com/sponsors/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-Donate-ff69b4.svg" alt="GitHub Sponsors">
</a>
<a href="https://www.buymeacoffee.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-ff69b4.svg" alt="Buy me a coffee">
</a>
<a href="https://ko-fi.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/kofi-Donate-ff69b4.svg" alt="Ko-fi">
</a>
<a href="https://twitter.com/dmlmont" target="_blank">
    <img src="https://img.shields.io/twitter/follow/dmlmont?style=social" alt="Twitter">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: <a href="https://github.com/davemlz/spyndex" target="_blank">https://github.com/davemlz/spyndex</a>

**Documentation**: *Under construction!*

**PyPI**: *Under construction!*

**conda-forge**: *Under construction!*

**Tutorials**: *Under construction!*

---

## Overview

The [Awesome Spectral Indices](https://github.com/davemlz/awesome-ee-spectral-indices) is a standardized ready-to-use curated list of spectral indices
that can be used as expressions for computing spectral indices in remote sensing applications. The list was born initially to supply spectral indices for
[Google Earth Engine]() through [eemont](https://github.com/davemlz/eemont) and [spectral](https://github.com/davemlz/spectral), but given the necessity to
compute spectral indices for other object classes outside the Earth Engine ecosystem, a new package was required.

Spyndex is a python package that uses the spectral indices from the *Awesome Spectral Indices* list and creates an expression evaluation method that is
compatible with python object classes that support [overloaded operators](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)
(e.g. [numpy.ndarray](https://github.com/numpy/numpy), [pandas.DataFrame](https://github.com/pandas-dev/pandas),
[xarray.DataArray](https://github.com/pydata/xarray)).

Check the simple usage of spyndex here:

```python
import spyndex
import numpy as np
import xarray as xr

N = np.random.normal(0.6,0.10,10000)
R = np.random.normal(0.1,0.05,10000)

da = xr.DataArray(
    np.array([N,R]).reshape(2,100,100),
    dims = ("band","x","y"),
    coords = {"band": ["NIR","Red"]}
)

idx = spyndex.computeIndex(
    index = ["NDVI","SAVI"],
    params = {
        "N": da.sel(band = "NIR"),
        "R": da.sel(band = "Red"),
        "L": 0.5
    }
)
```

## How does it work?

Any python object class that supports overloaded operators can be used with spyndex methods.

---

*"Hey... what do you mean by 'overloaded operators'?"*

---

That's the million dollars' question! An object class that supports overloaded operators is the one that allows you to compute operations like 
`a + b`, `a + b * c` or `(a - b) / (a + b)`. You know the last one, right? That's the formula of the famous [NDVI](https://doi.org/10.1016/0034-4257(79)90013-0).

So, if you can use the overloaded operators with an object class, you can use that class with [spyndex](https://github.com/davemlz/spyndex)!

Here is a little list of object classes that support overloaded operators:

- `float`
- `int`
- `numpy.ndarray` (with [numpy](https://github.com/numpy/numpy))
- `pandas.Series` (with [pandas](https://github.com/pandas-dev/pandas))
- `xarray.DataArray` (with [xarray](https://github.com/pydata/xarray))
- `ee.Image` (with [earthengine-api](https://github.com/google/earthengine-api) and [eemont](https://github.com/davemlz/eemont))

This means that you can actually use spyndex in a lot of processes! For example, you can download a Senitnel-2 image with
[sentinelsat](https://github.com/sentinelsat/sentinelsat), open and read it with [rasterio](https://github.com/mapbox/rasterio) and then compute the desired
spectral indices with [spyndex](https://github.com/davemlz/spyndex). Or you can search through the Landsat-8 STAC in the 
[Planetary Computer](https://planetarycomputer.microsoft.com/) ecosystem using [pystac_client](https://github.com/stac-utils/pystac-client),
convert it to an `xarray.DataArray` with [stackstac](https://github.com/gjoseph92/stackstac) and then compute spectral indices using
[spyndex](https://github.com/davemlz/spyndex)! Amazing, right!?

## Installation

Install the latest development version by running:

```
pip install git+https://github.com/davemlz/spyndex
```