import unittest

import ee
import eemont
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
            },
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)

    def test_numeric_class(self):
        """Test the computeIndex() method"""
        result = spyndex.indices.NDVI.compute(
            {
                "N": 0.6,
                "R": 0.1,
            },
        )
        self.assertIsInstance(result, float)

    def test_numeric_class_kwargs(self):
        """Test the computeIndex() method"""
        result = spyndex.indices.NDVI.compute(
            N = 0.6,
            R = 0.1,
        )
        self.assertIsInstance(result, float)

    def test_numeric_kwargs(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            N = 0.6,
            R = 0.1,
            G = 0.3,
            B = 0.1,
            L = spyndex.constants.L.default,
            C1 = spyndex.constants.C1.default,
            C2 = spyndex.constants.C2.default,
            g = spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
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
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
            },
            returnOrigin=False,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], xr.core.dataarray.DataArray)

    def test_ee(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": ee.Image(0.63),
                "R": ee.Image(0.13),
                "G": ee.Image(0.32),
                "B": ee.Image(0.12),
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
            },
        )
        self.assertIsInstance(result, ee.image.Image)

    def test_ee_origin_false(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            {
                "N": ee.Image(0.63),
                "R": ee.Image(0.13),
                "G": ee.Image(0.32),
                "B": ee.Image(0.12),
                "L": spyndex.constants.L.default,
                "C1": spyndex.constants.C1.default,
                "C2": spyndex.constants.C2.default,
                "g": spyndex.constants.g.default,
            },
            returnOrigin=False,
        )
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], ee.image.Image)


if __name__ == "__main__":
    unittest.main()
