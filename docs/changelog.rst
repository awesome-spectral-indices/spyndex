Changelog
=========

v0.7.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.7.0.
- Pinned latest versions: :code:`earthengine-api>=1.5.24`.
- :code:`pkg-resources` was removed `(#28) <https://github.com/awesome-spectral-indices/spyndex/issues/28>`_.
- Migrated from :code:`setup.py` to :code:`pyproject.toml` `(#20) <https://github.com/awesome-spectral-indices/spyndex/issues/20>`_.
- Refactor types `(#30) <https://github.com/awesome-spectral-indices/spyndex/pull/30>`_.

v0.6.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.6.0.

v0.5.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.5.0.
- Fixed heatmap plot `(#18) <https://github.com/awesome-spectral-indices/spyndex/issues/18>`_.
- Pinned latest versions: :code:`dask>=2023.7.0`, :code:`pandas>=2.0.3`, :code:`xarray>=2023.6.0`.

v0.4.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.4.0.

New Features
~~~~~~~~~~~~

- The :code:`common_name` attribute for the :code:`Band` class was created.
- The :code:`min_wavelength` attribute for the :code:`Band` class was created.
- The :code:`max_wavelength` attribute for the :code:`Band` class was created.

v0.3.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.3.0.

v0.2.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.2.0.
- :code:`Bands` and :code:`Constants` objects are automatically updated. 

v0.1.0
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.1.0.

v0.0.5
------

New Features
~~~~~~~~~~~~

- The :code:`SpectralIndices` class was created.
- The :code:`SpectralIndex` class was created.
- The :code:`Bands` class was created.
- The :code:`Band` class was created.
- The :code:`PlatformBand` class was created.
- The :code:`Constants` class was created.
- The :code:`Constant` class was created.

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.0.6.
- Added :code:`kwargs` argument to :code:`computeIndex`.
- Added :code:`kwargs` argument to :code:`computeKernel`.
- Added :code:`omega` to :code:`spyndex.constants`.
- Added :code:`k` to :code:`spyndex.constants`.
- Added :code:`PAR` to :code:`spyndex.constants`.
- Added :code:`lambdaG`, :code:`lambdaR` and :code:`lambdaN` to :code:`spyndex.constants`.

v0.0.4
------

Improvements
~~~~~~~~~~~~

- Awesome Spectral Indices list upgraded to v0.0.3.
- Fixed :code:`online` argument.

v0.0.3
------

Improvements
~~~~~~~~~~~~

- Added :code:`gamma` to :code:`spyndex.constants`. 

v0.0.2
------

Improvements
~~~~~~~~~~~~

- Fixed conflicts with coordinates for :code:`xarray.DataArray` objects when computing multiple indices.
- Local parameters are now used instead of global parameters.