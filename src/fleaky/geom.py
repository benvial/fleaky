#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: GPLv3

"""This module defines geometry and materials."""

import numpy as np
from dmsuite.poly_diff import Chebyshev


class Geometry:
    """The geometry."""

    def __init__(self, layers):
        """Create a geometry.

        Parameters
        ----------
        layers : _type_
            _description_
        """
        self.layers = layers
        self.thicknesses = [lay.thickness for lay in layers]
        self.radii = np.cumsum(self.thicknesses)


class Layer:
    """A layer."""

    def __init__(
        self,
        radius,
        thickness,
        material,
        disc,
        damping=None,
    ):
        """Create a layer.

        Parameters
        ----------
        radius : float >0
            The starting radius
        thickness : float >0
            Thickness of the layer
        material : Material
            The material the layer is made of
        disc : int
            Number of discretization points
        damping : float, optional
            The damping parameter for an infinite domain, by default None
        """
        self.radius = radius
        self.thickness = thickness
        self.material = material
        self.disc = disc
        self.damping = damping
        self.is_infinite = thickness == np.inf
        if self.is_infinite and damping == None:
            raise ValueError("Damping must be defined for an infinite layer!")
        self.cheb = Chebyshev(disc - 1)
        self.nodes = self.get_nodes()
        self.diff_matrices = [self.get_diff_matrix(i) for i in [1, 2]]

    def get_nodes(self):
        s = -self.cheb.nodes
        if self.is_infinite:
            return self.radius + self.thickness + self.damping * ((1 + s) / (1 - s))
        return self.radius + self.thickness * (1 + s) / 2

    def get_diff_matrix(self, order):
        if order not in [1, 2]:
            raise ValueError("Order must be 1 or 2!")

        if self.is_infinite:
            b = self.radius + self.thickness
            z_f = self.damping
            r_f = self.nodes
            D1 = -self.cheb.at_order(1)
            if order == 1:
                return np.diag((2 * z_f) / ((z_f + (r_f - b)) ** 2)) @ D1
            D2 = self.cheb.at_order(2)
            D2_f = np.diag((-4 * z_f) / ((z_f + (r_f - b)) ** 3)) @ D1
            D2_f += np.diag((4 * (z_f**2)) / ((z_f + (r_f - b)) ** 4)) @ D2
            return D2_f

        coeff = 2 / self.thickness
        if order == 1:
            return -self.cheb.at_order(1) * coeff
        return self.cheb.at_order(2) * coeff**2

    def get_S(self):
        D1, D2 = self.diff_matrices
        return D2 + np.diag(1 / self.nodes) @ D1


class Material:
    """Class representing a material."""

    def __init__(self, ρ, λ, μ):
        """Create a material.

        Parameters
        ----------
        ρ : float
            Mass density
        λ : float
            Lamé's first parameter
        μ : float
            Lamé's second parameter
        """
        self.ρ = ρ
        self.λ = λ
        self.μ = μ

    @property
    def transverse_wavespeed(self):
        """Transverse wavespeed."""
        return (self.μ / self.ρ) ** 0.5

    @property
    def longditudinal_wavespeed(self):
        """Longditudinal wavespeed."""
        return ((self.λ + 2 * self.μ) / self.ρ) ** 0.5

    @property
    def kappa(self):
        """Speeds ratio."""
        return self.longditudinal_wavespeed / self.transverse_wavespeed
