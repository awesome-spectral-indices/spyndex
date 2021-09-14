Getting Started
===============

Overview
--------

The `Awesome Spectral Indices <https://github.com/davemlz/awesome-spectral-indices>`_ is a standardized ready-to-use curated list of spectral indices
that can be used as expressions for computing spectral indices in remote sensing applications. The list was born initially to supply spectral 
indices for `Google Earth Engine <https://earthengine.google.com/>`_ through `eemont <https://github.com/davemlz/eemont>`_ and `spectral <https://github.com/davemlz/spectral>`_, but 
given the necessity to compute spectral indices for other object classes outside the Earth Engine ecosystem, a new package was required.

Spyndex is a python package that uses the spectral indices from the *Awesome Spectral Indices* list and creates an expression evaluation method that is
compatible with python object classes that support `overloaded operators <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>`_
(e.g. `numpy.ndarray <https://github.com/numpy/numpy>`_, `pandas.Series <https://github.com/pandas-dev/pandas>`_,
`xarray.DataArray <https://github.com/pydata/xarray>`_).

Some of the `spyndex` features are listed here:

- Access to Spectral Indices from the Awesome Spectral Indices list.
- Multiple Spectral Indices computation.
- Kernel Indices computation.
- Parallel processing.
- Compatibility with a lot of python objects!

Check the simple usage of spyndex here:

.. code-block:: python

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


How does it work?
-----------------

Any python object class that supports overloaded operators can be used with spyndex methods.

*"Hey... what do you mean by 'overloaded operators'?"*

That's the million dollars' question! An object class that supports overloaded operators is the one that allows you to compute mathematical 
operations using common operators (`+`, `-`, `/`, `*`, `**`) like `a + b`, `a + b * c` or `(a - b) / (a + b)`. You know the last one, right? That's 
the formula of the famous `NDVI <https://doi.org/10.1016/0034-4257(79)90013-0>`_.

So, if you can use the overloaded operators with an object class, you can use that class with `spyndex`!

> BE CAREFUL! Not all overloaded operators work as mathematical operators. In a `list` object class, the addition operator (`+`) concatenates two objects instead of performing an addition operation! So you must convert the `list` into a `numpy.ndarray` before using spyndex!

Here is a little list of object classes that support mathematical overloaded operators:

- `float` (Python Built-in type) or `numpy.float*` (with `numpy <https://github.com/numpy/numpy>`_)
- `int` (Python Built-in type) or `numpy.int*` (with `numpy <https://github.com/numpy/numpy>`_)
- `numpy.ndarray` (with `numpy <https://github.com/numpy/numpy>`_)
- `pandas.Series` (with `pandas <https://github.com/pandas-dev/pandas>`_ or `geopandas <https://github.com/geopandas/geopandas>`_)
- `xarray.DataArray` (with `xarray <https://github.com/pydata/xarray>`_)
- `ee.Image` (with `earthengine-api <https://github.com/google/earthengine-api>`_ and `eemont <https://github.com/davemlz/eemont>`_)
- `ee.Number` (with `earthengine-api <https://github.com/google/earthengine-api>`_ and `eemont <https://github.com/davemlz/eemont>`_)

And wait, there is more! If objects that support overloaded operatores can be used in spyndex, that means that you can work in **parallel**
with `dask <https://docs.dask.org/en/latest/>`_!

Here is the list of the dask objects that you can use with spyndex:

- `dask.array` (with `dask <https://docs.dask.org/en/latest/>`_)
- `dask.dataframe` (with `dask <https://docs.dask.org/en/latest/>`_)

This means that you can actually use spyndex in a lot of processes! For example, you can download a Sentinel-2 image with
`sentinelsat <https://github.com/sentinelsat/sentinelsat>`_, open and read it with `rasterio <https://github.com/mapbox/rasterio>`_ and then compute 
the desired spectral indices with `spyndex <https://github.com/davemlz/spyndex>`_. Or you can search through the Landsat-8 STAC in the 
`Planetary Computer <https://planetarycomputer.microsoft.com/>`_ ecosystem using `pystac-client <https://github.com/stac-utils/pystac-client>`_,
convert it to an `xarray.DataArray` with `stackstac <https://github.com/gjoseph92/stackstac>`_ and then compute spectral indices using
`spyndex <https://github.com/davemlz/spyndex>`_ in parallel with `dask <https://docs.dask.org/en/latest/>`_! Amazing, right!?

Installation
------------

Install the latest development version by running:

.. code-block::

    pip install git+https://github.com/davemlz/spyndex


Features
--------

Exploring Spectral Indices
~~~~~~~~~~~~~~~~~~~~~~~~~~

Spectral Indices from the Awesome Spectral Indices list can be accessed through
`spyndex.indices`. This is a `dictionary` where each one of the indices in the list
can be accessed as well as their `attributes <https://github.com/davemlz/awesome-ee-spectral-indices#attributes>`_:

.. code-block:: python

    import spyndex

    # All indices
    spyndex.indices

    # NDVI index
    spyndex.indices["NDVI"]

    # Formula of the NDVI
    spyndex.indices["NDVI"]["formula"]

    # Reference of the NDVI
    spyndex.indices["NDVI"]["reference"]


One (or more) Spectral Indices Computation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the `computeIndex()` method to compute as many spectral indices as you want!
The `index` parameter receives the spectral index or a list of spectral indices to
compute, while the `params` parameter receives a dictionary with the
`required parameters <https://github.com/davemlz/awesome-ee-spectral-indices#expressions>`_
for the spectral indices computation.

.. code-block:: python

    import spyndex
    import xarray as xr
    import matplotlib.pyplot as plt
    from rasterio import plot

    # Open a dataset (in this case a xarray.DataArray)
    snt = spyndex.datasets.open("sentinel")

    # Scale the data (remember that the valid domain for reflectance is [0,1])
    snt = snt / 10000

    # Compute the desired spectral indices
    idx = spyndex.computeIndex(
        index = ["NDVI","GNDVI","SAVI"],
        params = {
            "N": snt.sel(band = "B08"),
            "R": snt.sel(band = "B04"),
            "G": snt.sel(band = "B03"),
            "L": 0.5
        }
    )

    # Plot the indices (and the RGB image for comparison)
    fig, ax = plt.subplots(2,2,figsize = (10,10))
    plot.show(snt.sel(band = ["B04","B03","B02"]).data / 0.3,ax = ax[0,0],title = "RGB")
    plot.show(idx.sel(index = "NDVI"),ax = ax[0,1],title = "NDVI")
    plot.show(idx.sel(index = "GNDVI"),ax = ax[1,0],title = "GNDVI")
    plot.show(idx.sel(index = "SAVI"),ax = ax[1,1],title = "SAVI")


.. raw:: html

    <embed>
        <p align="center">
            <a href="https://github.com/davemlz/spyndex"><img src="https://raw.githubusercontent.com/davemlz/spyndex/main/docs/_static/sentinel.png" alt="sentinel spectral indices"></a>
        </p>
    </embed>

A `pandas.DataFrame`? Sure!
~~~~~~~~~~~~~~~~~~~~~~~~~~~

No matter what kind of python object you're working with, it can be used with `spyndex` as long as it supports mathematical overloaded operators! 

.. code-block:: python

    import spyndex
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Open a dataset (in this case a pandas.DataFrame)
    df = spyndex.datasets.open("spectral")

    # Compute the desired spectral indices
    idx = spyndex.computeIndex(
        index = ["NDVI","NDWI","NDBI"],
        params = {
            "N": df["SR_B5"],
            "R": df["SR_B4"],
            "G": df["SR_B3"],
            "S1": df["SR_B6"]
        }
    )

    # Add the land cover column to the result
    idx["Land Cover"] = df["class"]

    # Create a color palette for plotting
    colors = ["#E33F62","#3FDDE3","#4CBA4B"]

    # Plot a pairplot to check the indices behaviour
    plt.figure(figsize = (15,15))
    g = sns.PairGrid(idx,hue = "Land Cover",palette = sns.color_palette(colors))
    g.map_lower(sns.scatterplot)
    g.map_upper(sns.kdeplot,fill = True,alpha = .5)
    g.map_diag(sns.kdeplot,fill = True)
    g.add_legend()
    plt.show()


.. raw:: html

    <embed>
        <p align="center">
            <a href="https://github.com/davemlz/spyndex"><img src="https://raw.githubusercontent.com/davemlz/spyndex/main/docs/_static/spectral.png" alt="landsat spectral indices"></a>
        </p>
    </embed>

Parallel Processing
~~~~~~~~~~~~~~~~~~~

Parallel processing is possible with `spyndex` and `dask`! You can use `dask.array` or `dask.dataframe` objects to compute spectral indices with spyndex!
If you're using `xarray`, you can also define a chunk size and work in parallel!

.. code-block:: python

    import spyndex
    import numpy as np
    import dask.array as da

    # Define the array shape
    array_shape = (10000,10000)

    # Define the chunk size
    chunk_size = (1000,1000)

    # Create a dask.array object
    dask_array = da.array([
        da.random.normal(0.6,0.10,array_shape,chunks = chunk_size),
        da.random.normal(0.1,0.05,array_shape,chunks = chunk_size)
    ])

    # "Compute" the desired spectral indices
    idx = spyndex.computeIndex(
        index = ["NDVI","SAVI"],
        params = {
            "N": dask_array[0],
            "R": dask_array[1],
            "L": 0.5
        }
    )

    # Since dask works in lazy mode,
    # you have to tell it that you want to compute the indices!
    idx.compute()


Plotting Spectral Indices
~~~~~~~~~~~~~~~~~~~~~~~~~

All posible values of a spectral index can be visualized using `spyndex.plot.heatmap()`! This is a module that doesn't require data,
just specify the index, the bands, and BOOM! Heatmap of all the possible values of the index!

.. code-block:: python

    import spyndex
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Define subplots grid
    fig, ax = plt.subplots(1,2,figsize = (20,8))

    # Plot the NDVI with the Red values on the x-axis and the NIR on the y-axis
    ax[0].set_title("NDVI heatmap with default parameters")
    spyndex.plot.heatmap("NDVI","R","N",ax = ax[0])

    # Keywords arguments can be passed for sns.heatmap()
    ax[1].set_title("NDVI heatmap with seaborn keywords arguments")
    spyndex.plot.heatmap("NDVI","R","N",annot = True,cmap = "Spectral",ax = ax[1])

    plt.show()


.. raw:: html

    <embed>
        <p align="center">
        <a href="https://github.com/davemlz/spyndex"><img src="https://raw.githubusercontent.com/davemlz/spyndex/main/docs/_static/heatmap2.png" alt="heatmap"></a>
        </p>
    </embed>