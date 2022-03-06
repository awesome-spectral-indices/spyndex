from box import Box

from .utils import _get_indices
from .spyndex import computeIndex


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
        * Type: vegetation
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

        self.type = index["type"]
        """Type of the Spectral Index. One of ['vegetation', 'burn', 'water', 'urban', 'kernel', 'radar']"""

        self.reference = index["reference"]
        """URL to the reference/DOI of the Spectral Index."""

        self.formula = index["formula"].replace(" ","")
        """Formula (as expression) of the Spectral Index."""

        self.date_of_addition = index["date_of_addition"]
        """Date of addition of the Spectral Index to Awesome Spectral Indices."""

        self.contributor = index["contributor"]
        """Contributor of the Spectral Index to Awesome Spectral Indices."""

    def __repr__(self):
        """Machine readable output of the Spectral Index."""

        result = f"""SpectralIndex({self.short_name}: {self.long_name})
        * Type: {self.type}
        * Bands/Parameters: {self.bands}
        * Formula: {self.formula}
        * Reference: {self.reference}
        """    

        return result

    def __str__(self):
        """Human readable output of the Spectral Index."""

        result = f"""{self.short_name}: {self.long_name}
        * Type: {self.type}
        * Bands/Parameters: {self.bands}
        * Formula: {self.formula}
        * Reference: {self.reference}
        """    

        return result

    def compute(self, params = None, **kwargs):
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

        return computeIndex(self.short_name,parameters)


def _create_indices():
    """Creates the set of Spectral Indices locally available."""

    indices = _get_indices(False)
    indices_class = {}
    for key, value in indices.items():
        indices_class[key] = SpectralIndex(value)

    return SpectralIndices(indices_class,frozen_box = True)


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

    bands = {
        "A": {
            "short_name": "A",
            "long_name": "Aersols",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B1",
                "name": "Aerosols",
                "wavelength": 442.7,
                "bandwidth": 21
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B1",
                "name": "Aerosols",
                "wavelength": 442.3,
                "bandwidth": 21
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B1",
                "name": "Coastal Aerosol",
                "wavelength": 440.0,
                "bandwidth": 20.0
            },
            "landsat9": {
                "platform": "Landsat 8",
                "band": "B1",
                "name": "Coastal Aerosol",
                "wavelength": 440.0,
                "bandwidth": 20.0
            },
        },
        "B": {
            "short_name": "B",
            "long_name": "Blue",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B2",
                "name": "Blue",
                "wavelength": 492.4,
                "bandwidth": 66.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B2",
                "name": "Blue",
                "wavelength": 492.1,
                "bandwidth": 66.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B1",
                "name": "Blue",
                "wavelength": 485.0,
                "bandwidth": 70.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B1",
                "name": "Blue",
                "wavelength": 485.0,
                "bandwidth": 70.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B1",
                "name": "Blue",
                "wavelength": 485.0,
                "bandwidth": 70.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B2",
                "name": "Blue",
                "wavelength": 480.0,
                "bandwidth": 60.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B2",
                "name": "Blue",
                "wavelength": 480.0,
                "bandwidth": 60.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B3",
                "name": "Blue",
                "wavelength": 469.0,
                "bandwidth": 20.0
            },
        },
        "G": {
            "short_name": "G",
            "long_name": "Green",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B3",
                "name": "Green",
                "wavelength": 559.8,
                "bandwidth": 36.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B3",
                "name": "Green",
                "wavelength": 559.0,
                "bandwidth": 36.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B2",
                "name": "Green",
                "wavelength": 560.0,
                "bandwidth": 80.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B2",
                "name": "Green",
                "wavelength": 560.0,
                "bandwidth": 80.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B2",
                "name": "Green",
                "wavelength": 560.0,
                "bandwidth": 80.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B3",
                "name": "Green",
                "wavelength": 560.0,
                "bandwidth": 60.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B3",
                "name": "Green",
                "wavelength": 560.0,
                "bandwidth": 60.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B3",
                "name": "Green",
                "wavelength": 555.0,
                "bandwidth": 20.0
            },
        },
        "R": {
            "short_name": "R",
            "long_name": "Red",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B4",
                "name": "Red",
                "wavelength": 664.6,
                "bandwidth": 31.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B4",
                "name": "Red",
                "wavelength": 665.0,
                "bandwidth": 31.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B3",
                "name": "Red",
                "wavelength": 660.0,
                "bandwidth": 60.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B3",
                "name": "Red",
                "wavelength": 660.0,
                "bandwidth": 60.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B3",
                "name": "Red",
                "wavelength": 660.0,
                "bandwidth": 60.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B4",
                "name": "Red",
                "wavelength": 655.0,
                "bandwidth": 30.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B4",
                "name": "Red",
                "wavelength": 655.0,
                "bandwidth": 30.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B1",
                "name": "Red",
                "wavelength": 645.0,
                "bandwidth": 50.0
            },
        },
        "RE1": {
            "short_name": "RE1",
            "long_name": "Red Edge 1",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B5",
                "name": "Red Edge 1",
                "wavelength": 704.1,
                "bandwidth": 15.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B5",
                "name": "Red Edge 1",
                "wavelength": 703.8,
                "bandwidth": 15.0
            },
        },
        "RE2": {
            "short_name": "RE2",
            "long_name": "Red Edge 2",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B6",
                "name": "Red Edge 2",
                "wavelength": 740.5,
                "bandwidth": 15.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B6",
                "name": "Red Edge 2",
                "wavelength": 739.1,
                "bandwidth": 15.0
            },
        },
        "RE3": {
            "short_name": "RE3",
            "long_name": "Red Edge 3",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B7",
                "name": "Red Edge 3",
                "wavelength": 782.8,
                "bandwidth": 20.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B7",
                "name": "Red Edge 3",
                "wavelength": 779.7,
                "bandwidth": 20.0
            },
        },
        "RE4": {
            "short_name": "RE4",
            "long_name": "Near-Infrared (NIR) 2",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B8A",
                "name": "Near-Infrared (NIR) 2 (Red Edge 4 in Google Earth Engine)",
                "wavelength": 864.7,
                "bandwidth": 21.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B8A",
                "name": "Near-Infrared (NIR) 2 (Red Edge 4 in Google Earth Engine)",
                "wavelength": 864.0,
                "bandwidth": 21.0
            },
        },
        "N": {
            "short_name": "N",
            "long_name": "Near-Infrared (NIR)",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B8",
                "name": "Near-Infrared (NIR)",
                "wavelength": 832.8,
                "bandwidth": 106.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B8",
                "name": "Near-Infrared (NIR)",
                "wavelength": 833.0,
                "bandwidth": 106.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B4",
                "name": "Near-Infrared (NIR)",
                "wavelength": 830.0,
                "bandwidth": 140.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B4",
                "name": "Near-Infrared (NIR)",
                "wavelength": 830.0,
                "bandwidth": 140.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B4",
                "name": "Near-Infrared (NIR)",
                "wavelength": 835.0,
                "bandwidth": 130.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B5",
                "name": "Near-Infrared (NIR)",
                "wavelength": 865.0,
                "bandwidth": 30.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B5",
                "name": "Near-Infrared (NIR)",
                "wavelength": 865.0,
                "bandwidth": 30.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B1",
                "name": "Near-Infrared (NIR)",
                "wavelength": 858.5,
                "bandwidth": 35.0
            },
        },
        "S1": {
            "short_name": "S1",
            "long_name": "Short-wave Infrared (SWIR) 1",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B11",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1613.7,
                "bandwidth": 91.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B11",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1610.4,
                "bandwidth": 94.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B5",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1650.0,
                "bandwidth": 200.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B5",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1650.0,
                "bandwidth": 200.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B5",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1650.0,
                "bandwidth": 200.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B6",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1610.0,
                "bandwidth": 80.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B6",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1610.0,
                "bandwidth": 80.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B6",
                "name": "Short-wave Infrared (SWIR) 1",
                "wavelength": 1640.0,
                "bandwidth": 24.0
            },
        },
        "S2": {
            "short_name": "S2",
            "long_name": "Short-wave Infrared (SWIR) 2",
            "sentinel2a": {
                "platform": "Sentinel-2A",
                "band": "B12",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2202.4,
                "bandwidth": 175.0
            },
            "sentinel2b": {
                "platform": "Sentinel-2B",
                "band": "B12",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2185.7,
                "bandwidth": 185.0
            },
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2215.0,
                "bandwidth": 270.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2215.0,
                "bandwidth": 270.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2220.0,
                "bandwidth": 260.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2200.0,
                "bandwidth": 180.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2200.0,
                "bandwidth": 180.0
            },
            "modis": {
                "platform": "Terra/Aqua: MODIS",
                "band": "B7",
                "name": "Short-wave Infrared (SWIR) 2",
                "wavelength": 2130.0,
                "bandwidth": 50.0
            },
        },
        "T1": {
            "short_name": "T1",
            "long_name": "Thermal Infrared 1",
            "landsat4": {
                "platform": "Landsat 4",
                "band": "B6",
                "name": "Thermal Infrared 1",
                "wavelength": 11450.0,
                "bandwidth": 2100.0
            },
            "landsat5": {
                "platform": "Landsat 5",
                "band": "B6",
                "name": "Thermal Infrared 1",
                "wavelength": 11450.0,
                "bandwidth": 2100.0
            },
            "landsat7": {
                "platform": "Landsat 7",
                "band": "B6",
                "name": "Thermal Infrared 1",
                "wavelength": 11450.0,
                "bandwidth": 2100.0
            },
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B10",
                "name": "Thermal Infrared 1",
                "wavelength": 10895.0,
                "bandwidth": 590.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B10",
                "name": "Thermal Infrared 1",
                "wavelength": 10895.0,
                "bandwidth": 590.0
            },
        },
        "T2": {
            "short_name": "T2",
            "long_name": "Thermal Infrared 2",
            "landsat8": {
                "platform": "Landsat 8",
                "band": "B11",
                "name": "Thermal Infrared 2",
                "wavelength": 12005.0,
                "bandwidth": 1010.0
            },
            "landsat9": {
                "platform": "Landsat 9",
                "band": "B11",
                "name": "Thermal Infrared 2",
                "wavelength": 12005.0,
                "bandwidth": 1010.0
            },
        },
    }
    bands_class = {}
    for key, value in bands.items():
        bands_class[key] = Band(value)

    return Bands(bands_class,frozen_box = True)


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

    constants = {
        "L": {
            "short_name": "L",
            "description": "Canopy background adjustment",
            "default": 1.0,
        },
        "g": {
            "short_name": "g",
            "description": "Gain factor",
            "default": 2.5
        },
        "C1": {
            "short_name": "C1",
            "description": "Coefficient 1 for the aerosol resistance term",
            "default": 6.0,
        },
        "C2": {
            "short_name": "C2",
            "description": "Coefficient 2 for the aerosol resistance term",
            "default": 7.5,
        },
        "cexp": {
            "short_name": "cexp",
            "description": "Exponent used for OCVI",
            "default": 1.16,
        },
        "nexp": {
            "short_name": "nexp",
            "description": "Exponent used for GDVI",
            "default": 2.0,
        },
        "alpha": {
            "short_name": "alpha",
            "description": "Weighting coefficient used for WDRVI",
            "default": 0.1,
        },
        "gamma": {
            "short_name": "gamma",
            "description": "Weighting coefficient used for ARVI",
            "default": 1.0,
        },
        "omega": {
            "short_name": "omega",
            "description": "Weighting coefficient used for MBWI",
            "default": 2.0,
        },
        "k": {
            "short_name": "k",
            "description": "Slope parameter by soil used for NIRvH2",
            "default": 0.0,
        },
        "PAR": {
            "short_name": "PAR",
            "description": "Photosynthetically Active Radiation",
            "default": None,
        },
        "lambdaG": {
            "short_name": "lambdaG",
            "description": "Green wavelength (nm) used for NDGI",
            "default": None,
        },
        "lambdaR": {
            "short_name": "lambdaR",
            "description": "Red wavelength (nm) used for NIRvH2 and NDGI",
            "default": None,
        },
        "lambdaN": {
            "short_name": "lambdaN",
            "description": "NIR wavelength (nm) used for NIRvH2 and NDGI",
            "default": None,
        },
        "sla": {
            "short_name": "sla",
            "description": "Soil line slope",
            "default": 1.0,
        },
        "slb": {
            "short_name": "slb",
            "description": "Soil line intercept",
            "default": 0.0,
        },
        "sigma": {
            "short_name": "sigma",
            "description": "Length-scale parameter in the RBF kernel",
            "default": 0.5,
        },
        "p": {
            "short_name": "p",
            "description": "Kernel degree in the polynomial kernel",
            "default": 2.0,
        },
        "c": {
            "short_name": "c",
            "description": "Trade-off parameter in the polynomial kernel",
            "default": 1.0,
        },
    }
    constants_class = {}
    for key, value in constants.items():
        constants_class[key] = Constant(value)

    return Constants(constants_class,frozen_box = True)


constants = _create_constants()
