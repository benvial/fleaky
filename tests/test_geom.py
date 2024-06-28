"""Test cases for the geom module."""

import pytest


def test_material():
    import fleaky as fl

    mat = fl.Material(1, 2, 3)
    mat.transverse_wavespeed
    mat.longditudinal_wavespeed
    mat.kappa


def test_layer():
    import fleaky as fl
    import numpy as np

    mat = fl.Material(1, 2, 3)
    for damping in [None, 1.1 - 10j]:
        lay = fl.Layer(2, 2, [mat], 10, damping)
    with pytest.raises(ValueError):
        lay.get_diff_matrix(3)
    with pytest.raises(ValueError):
        lay = fl.Layer(1, np.inf, [mat], 10, None)
    lay = fl.Layer(1, np.inf, [mat], 10, 11 - 11j)


def test_geometry():
    import fleaky as fl

    mat = fl.Material(1, 2, 3)
    layers = []
    for damping in [None, 1 - 10j]:
        lay = fl.Layer(1, 2, [mat], 10, damping)
        layers.append(lay)

    geom = fl.Geometry(layers)
