from box import Box

from .spyndex import computeIndex
from .utils import _get_indices, _load_JSON


class SpectralIndices(Box):
    """Spectral Indices object.

    This object allows interaction with the complete list of Spectral Indices in the
    Awesome Spectral Indices list.

    See Also
    --------
    SpectralIndex : Spectral Index object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.indices
    SpectralIndices(['AFRI1600', 'AFRI2100', 'ARI', ..., 'kNDVI', 'kRVI', 'kVARI'])
    """

    def __repr__(self):
        """Machine readable output of the Spectral Indices object."""

        return f"SpectralIndices({list(self.keys())})"

    def __str__(self):
        """Human readable output of the Spectral Indices object."""

        return f"{list(self.keys())}"


class SpectralIndex(object):
    """Spectral Index object.

    This object allows interaction with specific Spectral Indices in the
    Awesome Spectral Indices list. Attributes of the Spectral Index can be accessed
    and the index itself can be computed.

    See Also
    --------
    SpectralIndices : Spectral Indices object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.indices.NIRv
    SpectralIndex(NIRv: Near-Infrared Reflectance of Vegetation)
        * Application Domain: vegetation
        * Bands/Parameters: ('N', 'R')
        * Formula: ((N-R)/(N+R))*N
        * Reference: https://doi.org/10.1126/sciadv.1602244
    >>> spyndex.indices.NIRv.contributor
    'https://github.com/davemlz'
    >>> spyndex.indices.NIRv.compute(N = 0.67,R = 0.12)
    0.4664556962025317
    """

    def __init__(self, index: dict):

        self.short_name = index["short_name"]
        """Short name of the Spectral Index."""

        self.long_name = index["long_name"]
        """Long name of the Spectral Index."""

        self.bands = index["bands"]
        """Required bands and parameters for the Spectral Index computation."""

        self.application_domain = index["application_domain"]
        """Appication domain of the Spectral Index. One of ['vegetation', 'burn', 'water', 'urban', 'kernel', 'radar']"""

        self.reference = index["reference"]
        """URL to the reference/DOI of the Spectral Index."""

        self.formula = index["formula"].replace(" ", "")
        """Formula (as expression) of the Spectral Index."""

        self.date_of_addition = index["date_of_addition"]
        """Date of addition of the Spectral Index to Awesome Spectral Indices."""

        self.contributor = index["contributor"]
        """Contributor of the Spectral Index to Awesome Spectral Indices."""

        self.platforms = index["platforms"]
        """Platforms with the required bands for the Spectral Index computation."""

    def __repr__(self):
        """Machine readable output of the Spectral Index."""

        result = f"""SpectralIndex({self.short_name}: {self.long_name})
        * Application Domain: {self.application_domain}
        * Bands/Parameters: {self.bands}
        * Formula: {self.formula}
        * Reference: {self.reference}
        """

        return result

    def __str__(self):
        """Human readable output of the Spectral Index."""

        result = f"""{self.short_name}: {self.long_name}
        * Application Domain: {self.application_domain}
        * Bands/Parameters: {self.bands}
        * Formula: {self.formula}
        * Reference: {self.reference}
        """

        return result

    def compute(self, params=None, **kwargs):
        """Computes a Spectral Index.

        Parameters
        ----------
        params: dict
            Parameters used as inputs for the computation. The input data must be
            compatible with Overloaded Operators. Some inputs' types supported are pandas
            series, numpy arrays, xarray objects and numeric objects. Earth Engine objects
            are also compatible when using eemont.
        kwargs:
            Parameters used as inputs for the computation as keyword pairs. Ignored when
            params is defined.

        Returns
        -------
        Any
            Computed Spectral Index.

        Examples
        --------
        Compute a Spectral Index by passing the required :code:`params` dictionary:

        >>> import spyndex
        >>> spyndex.indices.NDVI.compute(
        ...     params = {
        ...         "N": 0.643,
        ...         "R": 0.175
        ...     }
        ... )
        0.5721271393643031

        Compute a Spectral Index by passing the required :code:`params` as keyword pairs:

        >>> spyndex.indices.NDVI.compute(N = 0.643, R = 0.175, L = 0.5)
        0.5721271393643031
        """

        if params is None:
            parameters = kwargs
        else:
            parameters = params

        return computeIndex(self.short_name, parameters)


def _create_indices():
    """Creates the set of Spectral Indices locally available."""

    indices = _get_indices(False)
    indices_class = {}
    for key, value in indices.items():
        indices_class[key] = SpectralIndex(value)

    return SpectralIndices(indices_class, frozen_box=True)


indices = _create_indices()


class Bands(Box):
    """Bands object.

    This object allows interaction with the list of bands required for the Spectral
    Indices in the Awesome Spectral Indices list.

    See Also
    --------
    Band : Band object.
    PlatformBand : PlatformBand object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.bands
    Constants(['L', 'g', 'C1', ..., 'sigma', 'p', 'c'])
    """

    def __repr__(self):
        """Machine readable output of the Constant."""

        return f"Bands({list(self.keys())})"

    def __str__(self):
        """Human readable output of the Constant."""

        return f"{list(self.keys())}"


class PlatformBand(object):
    """Platform Band object.

    This object shows information about a specific band for a specific sensor or
    paltform.

    See Also
    --------
    Bands : Bands object.
    Band : Band object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.bands.B.sentinel2a
    PlatformBand(Platform: Sentinel-2A, Band: Blue)
        * Band: B2
        * Center Wavelength (nm): 492.4
        * Bandwidth (nm): 66.0
    >>> spyndex.bands.B.sentinel2a.wavelength
    492.4
    """

    def __init__(self, platform_band: dict):

        self.platform = platform_band["platform"]
        """Name of the Platform."""

        self.band = platform_band["band"]
        """Band number/name for the specific Platform."""

        self.name = platform_band["name"]
        """Description/Name of the Band for the specific Platform."""

        self.wavelength = platform_band["wavelength"]
        """Center wavelength of the Band (in nm) for the specific Platform."""

        self.bandwidth = platform_band["bandwidth"]
        """Bandwidth of the Band (in nm) for the specific Platform."""

    def __repr__(self):
        """Machine readable output of the Band."""

        result = f"""PlatformBand(Platform: {self.platform}, Band: {self.name})
        * Band: {self.band}
        * Center Wavelength (nm): {self.wavelength}
        * Bandwidth (nm): {self.bandwidth}
        """

        return result

    def __str__(self):
        """Human readable output of the Band."""

        result = f"""Platform: {self.platform}, Band: {self.name}
        * Band: {self.band}
        * Center Wavelength (nm): {self.wavelength}
        * Bandwidth (nm): {self.bandwidth}
        """

        return result


class Band(object):
    """Band object.

    This object allows interaction with specific bands in the the list of required bands
    for the Spectral Indices in the Awesome Spectral Indices list. Attributes of the
    Band can be accessed using this object.

    See Also
    --------
    Bands : Bands object.
    PlatformBand : PlatformBand object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.bands.B
    Band(B: Blue)
    >>> spyndex.bands.B.long_name
    'Blue'
    """

    def __init__(self, band: dict):

        self.short_name = band["short_name"]
        """Short name of the Band."""

        self.long_name = band["long_name"]
        """Description/Name of the Band."""

        self.standard = band["short_name"]
        """Short name of the Band. Equivalent to :code:`short_name`."""

        if "sentinel2a" in band.keys():
            self.sentinel2a = PlatformBand(band["sentinel2a"])
            """Description of the band for the Sentinel-2A platform."""

        if "sentinel2b" in band.keys():
            self.sentinel2b = PlatformBand(band["sentinel2b"])
            """Description of the band for the Sentinel-2B platform."""

        if "landsat4" in band.keys():
            self.landsat4 = PlatformBand(band["landsat4"])
            """Description of the band for the Landsat 4 platform."""

        if "landsat5" in band.keys():
            self.landsat5 = PlatformBand(band["landsat5"])
            """Description of the band for the Landsat 5 platform."""

        if "landsat7" in band.keys():
            self.landsat7 = PlatformBand(band["landsat7"])
            """Description of the band for the Landsat 7 platform."""

        if "landsat8" in band.keys():
            self.landsat8 = PlatformBand(band["landsat8"])
            """Description of the band for the Landsat 8 platform."""

        if "landsat9" in band.keys():
            self.landsat9 = PlatformBand(band["landsat9"])
            """Description of the band for the Landsat 9 platform."""

        if "modis" in band.keys():
            self.modis = PlatformBand(band["modis"])
            """Description of the band for the MODIS platform."""

    def __repr__(self):
        """Machine readable output of the Band."""

        result = f"""Band({self.short_name}: {self.long_name})
        """

        return result

    def __str__(self):
        """Human readable output of the Constant."""

        result = f"""{self.short_name}: {self.long_name}
        """

        return result


def _create_bands():
    """Creates the set of Bands locally available."""

    bands = _load_JSON("bands.json")
    bands_class = {}
    for key, value in bands.items():
        bands_class[key] = Band(value)

    return Bands(bands_class, frozen_box=True)


bands = _create_bands()


class Constants(Box):
    """Constants object.

    This object allows interaction with the list of constants of the Spectral Indices in
    the Awesome Spectral Indices list.

    See Also
    --------
    Constant : Constant object.
    Bands : Bands object.
    SpectralIndex: Spectral Index object.
    SpectralIndices : Spectral Indices object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.constants
    Constants(['L', 'g', 'C1', ..., 'sigma', 'p', 'c'])
    """

    def __repr__(self):
        """Machine readable output of the Constants object."""

        return f"Constants({list(self.keys())})"

    def __str__(self):
        """Human readable output of the Constants object."""

        return f"{list(self.keys())}"


class Constant(object):
    """Constant object.

    This object allows interaction with specific constants in the the list of constants of
    the Spectral Indices in  the Awesome Spectral Indices list. Attributes of the
    Constant can be accessed using this object.

    See Also
    --------
    Constants : Constants object.
    Bands : Bands object.
    SpectralIndex: Spectral Index object.
    SpectralIndices : Spectral Indices object.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.constants.L
    Constant(L: Canopy background adjustment)
        * Default value: 1.0
    >>> spyndex.constants.L.default
    1.0
    """

    def __init__(self, constant: dict):

        self.description = constant["description"]
        """Description/Name of the Constant."""

        self.long_name = constant["description"]
        """Description/Name of the Constant. Equivalent to :code:`description`."""

        self.short_name = constant["short_name"]
        """Short name of the Constant."""

        self.standard = constant["short_name"]
        """Short name of the Constant. Equivalent to :code:`short_name`."""

        self.default = constant["default"]
        """Default value of the Constant."""

        self.value = constant["default"]
        """Default value of the Constant. Equivalent to :code:`default`."""

    def __repr__(self):
        """Machine readable output of the Constant."""

        result = f"""Constant({self.short_name}: {self.long_name})
        * Default value: {self.default}
        """

        return result

    def __str__(self):
        """Human readable output of the Constant."""

        result = f"""{self.short_name}: {self.long_name}
        * Default value: {self.default}
        """

        return result


def _create_constants():
    """Creates the set of Constants locally available."""

    constants = _load_JSON("constants.json")
    constants_class = {}
    for key, value in constants.items():
        constants_class[key] = Constant(value)

    return Constants(constants_class, frozen_box=True)


constants = _create_constants()
