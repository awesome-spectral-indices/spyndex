API Reference
=============

Here you will find all spyndex methods:

spyndex.spyndex
---------------

Core module of spyndex. All functions here are automatically loaded with :code:`import spyndex`
and can be called from it (e.g., :code:`spyndex.computeIndex()`):

.. currentmodule:: spyndex.spyndex

.. autosummary::
   :toctree: stubs

   computeIndex
   computeKernel

spyndex.axioms
---------------

Axioms module of spyndex. Automatically loaded with :code:`import spyndex`. Spectral Indices, Constants and Bands
can be accessed from the module (e.g. :code:`spyndex.indices.NDVI`):

.. currentmodule:: spyndex.axioms

.. autosummary::

   SpectralIndices
   SpectralIndex


spyndex.datasets
----------------

Example datasets. Automatically loaded with :code:`import spyndex`. Functions from this
module can be loaded from the module (e.g., :code:`spyndex.datasets.open()`):

.. currentmodule:: spyndex.datasets

.. autosummary::
   :toctree: stubs

   open

spyndex.plot
------------

Plotting indices. Automatically loaded with :code:`import spyndex`. Functions from this
module can be loaded from the module (e.g., :code:`spyndex.plot.heatmap()`):

.. currentmodule:: spyndex.plot

.. autosummary::
   :toctree: stubs

   heatmap