from typing import Optional, Union

import numpy as np
import pandas as pd
import seaborn as sns

import spyndex

from .utils import _check_params, _get_indices


def heatmap(index: str, x: str, y: str, params: Optional[dict] = None, **kwargs):
    """Plot all posible index values as a color-encoded matrix.

    Parameters
    ----------
    index : str
        Index to plot.
    x : str
        Band to plot in the x-axis.
    y : str
        Band to plot in the y-axis.
    params: dict
        Parameters for all remaining bands that are not used in :code:`x` nor :code:`y`.
        This dictionary must store just float values.
    **kwargs : Keyword arguments
        Keyword arguments that can be passed to :code:`seaborn.heatmap()`.

    Returns
    -------
    Matplotlib Axes
        Axes object with the index heatmap.

    Examples
    --------
    >>> import spyndex
    >>> spyndex.plot.heatmap("NDVI","N","R",cmap = "Spectral",annot = True)

    If the index uses more than one band, the remaining bands or parameters must
    be passed in the :code:`params` dictionary.

    >>> spyndex.plot.heatmap(
    ...    "SAVI",
    ...    "N",
    ...    "R",
    ...    params = {"L": 0.5},
    ...    cmap = "Spectral",
    ...    annot = True)
    """

    grid = np.round(np.mgrid[0:1.1:0.1, 0:1.1:0.1], 1)
    X = grid[0].flatten()
    Y = grid[1].flatten()

    df = pd.DataFrame(
        {
            x: X,
            y: Y,
        }
    )

    if params is not None:
        params = {**params, x: df[x], y: df[y]}
    else:
        params = {x: df[x], y: df[y]}

    _check_params(index, params)

    df[index] = spyndex.computeIndex(index=index, params=params)

    df = df.pivot(y, x, index)

    h = sns.heatmap(df, **kwargs)
    h.invert_yaxis()

    return h
