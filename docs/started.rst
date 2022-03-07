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

Some of the :code:`spyndex` features are listed here:

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

Bands can also be passed as keywords arguments:

.. code-block:: python

    idx = spyndex.computeIndex(
        index = ["NDVI","SAVI"],
        N = da.sel(band = "NIR"),
        R = da.sel(band = "Red"),
        L = 0.5
    )

And indices can be computed from their class:

.. code-block:: python

    idx = spyndex.indices.NDVI.compute(
        N = da.sel(band = "NIR"),
        R = da.sel(band = "Red"),
    )

How does it work?
-----------------

Any python object class that supports overloaded operators can be used with spyndex methods.

*"Hey... what do you mean by 'overloaded operators'?"*

That's the million dollars' question! An object class that supports overloaded operators is the one that allows you to compute mathematical 
operations using common operators (:code:`+`, :code:`-`, :code:`/`, :code:`*`, :code:`**`) like :code:`a + b`, :code:`a + b * c` or :code:`(a - b) / (a + b)`. You know the last one, right? That's 
the formula of the famous `NDVI <https://doi.org/10.1016/0034-4257(79)90013-0>`_.

So, if you can use the overloaded operators with an object class, you can use that class with `spyndex`!

> BE CAREFUL! Not all overloaded operators work as mathematical operators. In a :code:`list` object class, the addition operator (:code:`+`) concatenates two objects instead of performing an addition operation! So you must convert the :code:`list` into a :code:`numpy.ndarray` before using spyndex!

Here is a little list of object classes that support mathematical overloaded operators:

- :code:`float` (Python Built-in type) or :code:`numpy.float*` (with `numpy <https://github.com/numpy/numpy>`_)
- :code:`int` (Python Built-in type) or :code:`numpy.int*` (with `numpy <https://github.com/numpy/numpy>`_)
- :code:`numpy.ndarray` (with `numpy <https://github.com/numpy/numpy>`_)
- :code:`pandas.Series` (with `pandas <https://github.com/pandas-dev/pandas>`_ or `geopandas <https://github.com/geopandas/geopandas>`_)
- :code:`xarray.DataArray` (with `xarray <https://github.com/pydata/xarray>`_)
- :code:`ee.Image` (with `earthengine-api <https://github.com/google/earthengine-api>`_ and `eemont <https://github.com/davemlz/eemont>`_)
- :code:`ee.Number` (with `earthengine-api <https://github.com/google/earthengine-api>`_ and `eemont <https://github.com/davemlz/eemont>`_)

And wait, there is more! If objects that support overloaded operatores can be used in spyndex, that means that you can work in **parallel**
with `dask <https://docs.dask.org/en/latest/>`_!

Here is the list of the dask objects that you can use with spyndex:

- :code:`dask.Array` (with `dask <https://docs.dask.org/en/latest/>`_)
- :code:`dask.Series` (with `dask <https://docs.dask.org/en/latest/>`_)

This means that you can actually use spyndex in a lot of processes! For example, you can download a Sentinel-2 image with
`sentinelsat <https://github.com/sentinelsat/sentinelsat>`_, open and read it with `rasterio <https://github.com/mapbox/rasterio>`_ and then compute 
the desired spectral indices with `spyndex <https://github.com/davemlz/spyndex>`_. Or you can search through the Landsat-8 STAC in the 
`Planetary Computer <https://planetarycomputer.microsoft.com/>`_ ecosystem using `pystac-client <https://github.com/stac-utils/pystac-client>`_,
convert it to an :code:`xarray.DataArray` with `stackstac <https://github.com/gjoseph92/stackstac>`_ and then compute spectral indices using
`spyndex <https://github.com/davemlz/spyndex>`_ in parallel with `dask <https://docs.dask.org/en/latest/>`_! Amazing, right!?

Installation
------------

Install the latest version from PyPI:

.. code-block::
    
    pip install spyndex


Upgrade spyndex by running:

.. code-block::
    
    pip install -U spyndex


Install the latest version from conda-forge:

.. code-block::

    conda install -c conda-forge spyndex


Install the latest dev version from GitHub by running:

.. code-block::

    pip install git+https://github.com/davemlz/spyndex


Features
--------

Exploring Spectral Indices
~~~~~~~~~~~~~~~~~~~~~~~~~~

Spectral Indices from the Awesome Spectral Indices list can be accessed through
:code:`spyndex.indices`. This is a :code:`dictionary` where each one of the indices in the 
list can be accessed as well as their `attributes <https://github.com/davemlz/awesome-ee-spectral-indices#attributes>`_:

.. code-block:: python

    import spyndex

    # All indices
    spyndex.indices

    # NDVI index
    spyndex.indices["NDVI"]

    # Or with dot notation
    spyndex.indices.NDVI

    # Formula of the NDVI
    spyndex.indices["NDVI"]["formula"]

    # Or with dot notation
    spyndex.indices.NDVI.formula

    # Reference of the NDVI
    spyndex.indices["NDVI"]["reference"]

    # Or with dot notation
    spyndex.indices.NDVI.reference


Default Values
~~~~~~~~~~~~~~

Some Spectral Indices require constant values in order to be computed. Default values
can be accessed through :code:`spyndex.constants`. This is a :code:`Box` object
where each one of the `constants <https://github.com/davemlz/awesome-spectral-indices#expressions>`_ can be
accessed:

.. code-block:: python

    import spyndex

    # All constants
    spyndex.constants

    # Canopy Background Adjustment
    spyndex.constants["L"]

    # Or with dot notation
    spyndex.constants.L

    # Default value
    spyndex.constants["L"]["default"]

    # Or with dot notation
    spyndex.constants.L.default


Band Parameters
~~~~~~~~~~~~~~~

The standard band parameters description can be accessed through :code:`spyndex.bands`. This is 
a :code:`Box` object where each one of the `bands <https://github.com/davemlz/awesome-spectral-indices#expressions>`_ 
can be accessed:

.. code-block:: python

    import spyndex

    # All bands
    spyndex.bands

    # Blue band
    spyndex.bands["B"]

    # Or with dot notation
    spyndex.bands.B


One (or more) Spectral Indices Computation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the :code:`computeIndex()` method to compute as many spectral indices as you want!
The :code:`index` parameter receives the spectral index or a list of spectral indices to
compute, while the :code:`params` parameter receives a dictionary with the
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

Kernel Indices Computation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the :code:`computeKernel()` method to compute the required kernel for kernel indices like
the kNDVI! The :code:`kernel` parameter receives the kernel to compute, while the :code:`params` 
parameter receives a dictionary with the
`required parameters <https://github.com/davemlz/awesome-ee-spectral-indices#expressions>`_
for the kernel computation (e.g., :code:`a`, :code:`b` and :code:`sigma` for the RBF kernel).

.. code-block:: python

    import spyndex
    import xarray as xr
    import matplotlib.pyplot as plt
    from rasterio import plot

    # Open a dataset (in this case a xarray.DataArray)
    snt = spyndex.datasets.open("sentinel")

    # Scale the data (remember that the valid domain for reflectance is [0,1])
    snt = snt / 10000

    # Compute the kNDVI and the NDVI for comparison
    idx = spyndex.computeIndex(
        index = ["NDVI","kNDVI"],
        params = {
            # Parameters required for NDVI
            "N": snt.sel(band = "B08"),
            "R": snt.sel(band = "B04"),
            # Parameters required for kNDVI
            "kNN" : 1.0,
            "kNR" : spyndex.computeKernel(
                kernel = "RBF",
                params = {
                    "a": snt.sel(band = "B08"),
                    "b": snt.sel(band = "B04"),
                    "sigma": snt.sel(band = ["B08","B04"]).mean("band")
                }),
        }
    )

    # Plot the indices (and the RGB image for comparison)
    fig, ax = plt.subplots(1,3,figsize = (15,15))
    plot.show(snt.sel(band = ["B04","B03","B02"]).data / 0.3,ax = ax[0],title = "RGB")
    plot.show(idx.sel(index = "NDVI"),ax = ax[1],title = "NDVI")
    plot.show(idx.sel(index = "kNDVI"),ax = ax[2],title = "kNDVI")


.. raw:: html

    <embed>
        <p align="center">
            <a href="https://github.com/davemlz/spyndex"><img src="https://raw.githubusercontent.com/davemlz/spyndex/main/docs/_static/kNDVI.png" alt="sentinel kNDVI"></a>
        </p>
    </embed>

A `pandas.DataFrame`? Sure!
~~~~~~~~~~~~~~~~~~~~~~~~~~~

No matter what kind of python object you're working with, it can be used with 
:code:`spyndex` as long as it supports mathematical overloaded operators! 

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

Parallel processing is possible with :code:`spyndex` and :code:`dask`! You can use 
:code:`dask.Array` or :code:`dask.DataFrame` objects to compute spectral indices with 
spyndex! If you're using :code:`xarray`, you can also define a chunk size and work in 
parallel!

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

All posible values of a spectral index can be visualized using 
:code:`spyndex.plot.heatmap()`! This is a module that doesn't require data,
just specify the index, the bands, and BOOM! Heatmap of all the possible values of the 
index!

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