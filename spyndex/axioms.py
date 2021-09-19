from box import Box

from .utils import _get_indices


class SpectralIndices(Box):
    def __repr__(self):
        keys = list(self.keys())
        if "short_name" in keys:
            toShow = f"{self['short_name']}: {self['long_name']} (attributes = {keys})"
        else:
            toShow = f"SpectralIndices({list(self.keys())})"
        return toShow


indices = SpectralIndices(_get_indices(False), frozen_box=True)


class Bands(Box):
    def __repr__(self):
        return f"Bands({self})"


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
    def __repr__(self):
        keys = list(self.keys())
        if "description" in keys:
            toShow = f"{self['description']} (default = {self['default']})"
        else:
            toShow = f"Constants({list(self.keys())})"
        return toShow


constants = Constants(
    {
        "L": {"description": "Canopy background adjustment", "default": 1.0},
        "g": {"description": "Gain factor", "default": 2.5},
        "C1": {
            "description": "Coefficient 1 for the aerosol resistance term",
            "default": 6.0,
        },
        "C2": {
            "description": "Coefficient 2 for the aerosol resistance term",
            "default": 7.5,
        },
        "cexp": {"description": "Exponent used for OCVI", "default": 1.16},
        "nexp": {"description": "Exponent used for GDVI", "default": 2.0},
        "alpha": {
            "description": "Weighting coefficient used for WDRVI",
            "default": 0.1,
        },
        "sla": {"description": "Soil line slope", "default": 1.0},
        "slb": {"description": "Soil line intercept", "default": 0.0},
        "sigma": {
            "description": "Length-scale parameter in the RBF kernel",
            "default": 0.5,
        },
        "p": {"description": "Kernel degree in the polynomial kernel", "default": 2.0},
        "c": {
            "description": "Trade-off parameter in the polynomial kernel",
            "default": 1.0,
        },
    },
    frozen_box=True,
)
