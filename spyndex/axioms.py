from .utils import _get_indices

indices = _get_indices(False)

defaultParameters = {
    "L": 1.0,
    "g": 2.5,
    "C1": 6.0,
    "C2": 7.5,
    "cexp": 1.16,
    "nexp": 2.0,
    "alpha": 0.1,
    "sla": 1.0,
    "slb": 0.0,
    "p": 2.0,
    "c": 1.0,
}

describeParameters = {
    "Bands": {
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
    "Additional Parameters": {
        "Index Parameters": {
            "L": "Canopy background adjustment",
            "g": "Gain factor",
            "C1": "Coefficient 1 for the aerosol resistance term",
            "C2": "Coefficient 2 for the aerosol resistance term",
            "cexp": "Exponent used for OCVI",
            "nexp": "Exponent used for GDVI",
            "alpha": "Weighting coefficient used for WDRVI",
            "sla": "Soil line slope",
            "slb": "Soil line intercept",
        },
        "Kernel Parameters": {
            "sigma": "Length-scale parameter in the RBF kernel",
            "p": "Kernel degree in the polynomial kernel",
            "c": "Trade-off parameter in the polynomial kernel",
        },
    },
}
