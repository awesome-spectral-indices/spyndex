import unittest

import dask
import dask.array
import dask.dataframe
import numpy as np
import pandas as pd
import xarray as xr

import spyndex

try:
    import ee
    import eemont
    ee.Initialize()
    HAS_EE = True
except ImportError:
    HAS_EE = False

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

    def test_catalogue_indices(self):
        """Test the indices class"""
        self.assertIsInstance(spyndex.indices.NDVI.platforms, list)
        self.assertIsInstance(spyndex.indices.NDVI.application_domain, str)

    def test_catalogue_bands(self):
        """Test the bands class"""
        self.assertIsInstance(spyndex.bands.N.short_name, str)
        self.assertIsInstance(spyndex.bands.N.sentinel2a.wavelength, float)

    def test_catalogue_constants(self):
        """Test the constants class"""
        self.assertIsInstance(spyndex.constants.C1.short_name, str)

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
            N=0.6,
            R=0.1,
        )
        self.assertIsInstance(result, float)

    def test_numeric_kwargs(self):
        """Test the computeIndex() method"""
        result = spyndex.computeIndex(
            indices,
            N=0.6,
            R=0.1,
            G=0.3,
            B=0.1,
            L=spyndex.constants.L.default,
            C1=spyndex.constants.C1.default,
            C2=spyndex.constants.C2.default,
            g=spyndex.constants.g.default,
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
        self.assertIsInstance(result, pd.DataFrame)

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
        self.assertIsInstance(result[0], pd.Series)

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
        self.assertIsInstance(result, xr.DataArray)

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
        self.assertIsInstance(result[0], xr.DataArray)

    @unittest.skipUnless(HAS_EE, "Earth Engine not installed")
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
        self.assertIsInstance(result, ee.Image)

    @unittest.skipUnless(HAS_EE, "Earth Engine not installed")
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
        self.assertIsInstance(result[0], ee.Image)


    def test_dtype_numeric(self):
        """Test the dtype parameter with numeric inputs"""
        result = spyndex.computeIndex(
            "NDVI",
            {
                "N": 0.6,
                "R": 0.1,
            },
            dtype="float32",
        )
        self.assertIsInstance(result, np.float32)

    def test_dtype_numpy(self):
        """Test the dtype parameter with numpy arrays"""
        N_uint16 = (N * 10000).astype("uint16")
        R_uint16 = (R * 10000).astype("uint16")

        result_default = spyndex.computeIndex(
            "NDVI",
            {
                "N": N_uint16 / 10000,
                "R": R_uint16 / 10000,
            },
        )
        self.assertEqual(result_default.dtype, np.float64)

        result_cast = spyndex.computeIndex(
            "NDVI",
            {
                "N": N_uint16 / 10000,
                "R": R_uint16 / 10000,
            },
            dtype="float32",
        )
        self.assertEqual(result_cast.dtype, np.float32)

    def test_dtype_numpy_multiple(self):
        """Test the dtype parameter with numpy arrays and multiple indices"""
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
            dtype="float32",
        )
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, np.float32)

    def test_dtype_pandas(self):
        """Test the dtype parameter with pandas Series"""
        result = spyndex.computeIndex(
            "NDVI",
            {
                "N": df["N"],
                "R": df["R"],
            },
            dtype="float32",
        )
        self.assertEqual(result.dtype, np.float32)

    def test_dtype_xarray(self):
        """Test the dtype parameter with xarray DataArrays"""
        result = spyndex.computeIndex(
            "NDVI",
            {
                "N": da.sel(channel="N"),
                "R": da.sel(channel="R"),
            },
            dtype="float32",
        )
        self.assertEqual(result.dtype, np.float32)

    def test_dtype_class(self):
        """Test the dtype parameter through SpectralIndex.compute()"""
        result = spyndex.indices.NDVI.compute(
            {
                "N": 0.6,
                "R": 0.1,
            },
            dtype="float32",
        )
        self.assertIsInstance(result, np.float32)

    def test_dtype_kernel(self):
        """Test the dtype parameter through computeKernel()"""
        result = spyndex.computeKernel(
            "linear",
            {
                "a": N,
                "b": R,
            },
            dtype="float32",
        )
        self.assertEqual(result.dtype, np.float32)

    def test_dtype_invalid(self):
        """Test that an invalid dtype raises an exception"""
        with self.assertRaises(TypeError):
            spyndex.computeIndex(
                "NDVI",
                {
                    "N": 0.6,
                    "R": 0.1,
                },
                dtype="not_a_dtype",
            )

    def test_dtype_does_not_mutate_params(self):
        """Test that the original params dict is not mutated"""
        params = {"N": N, "R": R}
        spyndex.computeIndex("NDVI", params, dtype="float32")
        self.assertEqual(params["N"].dtype, np.float64)
        self.assertEqual(params["R"].dtype, np.float64)


if __name__ == "__main__":
    unittest.main()
