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

    This object allows interaction with the bands of Spectral Indices in the
    Awesome Spectral Indices list according to their standard names.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.bands
    Bands({'A': 'Aerosols band', 'B': 'Blue band', ..., 'T2': 'Thermal band 2'})
    >>> spyndex.bands.B
    'Blue band'
    """

    def __repr__(self):
        """Machine readable output of the Bands object."""

        return f"Bands({self})"

    def __str__(self):
        """Human readable output of the Bands object."""

        return f"{self}"


bands = Bands(
    {
        "A": "Aerosols band",
        "B": "Blue band",
        "G": "Green band",
        "R": "Red band",
        "RE1": "Red Edge band 1",
        "RE2": "Red Edge band 2",
        "RE3": "Red Edge band 3",
        "RE4": "Red Edge band 4",
        "N": "Near Infrared band",
        "S1": "SWIR band 1",
        "S2": "SWIR band 2",
        "T1": "Thermal band 1",
        "T2": "Thermal band 2",
    },
    frozen_box=True,
)


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
