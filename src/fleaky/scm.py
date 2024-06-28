#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: GPLv3


from dmsuite.poly_diff import Chebyshev, DiffMatOnDomain

N_f = 5
cheb = Chebyshev(N_f - 1)

s = -cheb.nodes

a = 0
b=1
h = b-a
r_a = (h * s + a + b) / 2
print(r_a)



a = 1
b=2.5
h = b-a
r_b = (h * s + a + b) / 2
print(r_b)

