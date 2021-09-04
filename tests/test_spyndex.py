import unittest

import ee
import numpy as np
import pandas as pd
import xarray as xr

import spyndex

ee.Initialize()

B = np.random.normal(0.1, 0.1, 20 * 20)
G = np.random.normal(0.3, 0.1, 20 * 20)
R = np.random.normal(0.1, 0.1, 20 * 20)
N = np.random.normal(0.6, 0.1, 20 * 20)

df = pd.DataFrame({"B": B, "G": G, "R": R, "N": N})

da = xr.DataArray(
    np.array(
        [
            B.reshape(20, 20),
            G.reshape(20, 20),
            R.reshape(20, 20),
            N.reshape(20, 20),
        ]
    ),
    dims=("channel", "x", "y"),
    coords={"channel": ["B", "G", "R", "N"]},
)

indices = ["NDVI", "GNDVI", "SAVI", "EVI"]


class Test(unittest.TestCase):
    """Tests for the spyndex package."""

    def test_numeric(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": 0.6,
                "R": 0.1,
                "G": 0.3,
                "B": 0.1,
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)

    def test_numeric_online(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": 0.6,
                "R": 0.1,
                "G": 0.3,
                "B": 0.1,
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
            online=True,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)

    def test_numpy(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": N,
                "R": R,
                "G": G,
                "B": B,
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
        )
        self.assertIsInstance(result, np.ndarray)

    def test_numpy_origin_false(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": N,
                "R": R,
                "G": G,
                "B": B,
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
            returnOrigin=False,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], np.ndarray)

    def test_pandas(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": df["N"],
                "R": df["R"],
                "G": df["G"],
                "B": df["B"],
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
        )
        self.assertIsInstance(result, pd.core.frame.DataFrame)

    def test_pandas_origin_false(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": df["N"],
                "R": df["R"],
                "G": df["G"],
                "B": df["B"],
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
            returnOrigin=False,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], pd.core.series.Series)

    def test_xarray(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": da.sel(channel="N"),
                "R": da.sel(channel="R"),
                "G": da.sel(channel="G"),
                "B": da.sel(channel="B"),
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
        )
        self.assertIsInstance(result, xr.core.dataarray.DataArray)

    def test_xarray_origin_false(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": da.sel(channel="N"),
                "R": da.sel(channel="R"),
                "G": da.sel(channel="G"),
                "B": da.sel(channel="B"),
                "L": spyndex.defaultParameters["L"],
                "C1": spyndex.defaultParameters["C1"],
                "C2": spyndex.defaultParameters["C2"],
                "g": spyndex.defaultParameters["g"],
            },
            returnOrigin=False,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], xr.core.dataarray.DataArray)


if __name__ == "__main__":
    unittest.main()
