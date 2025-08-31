import math


g = 9.81


def eq1(v, v0, a): # V = V0 + at
    return (v - v0) / a

def eq2(t, v0, a): # S = V0t + (1/2)at^2
    return v0 * t + 0.5 * a * t**2

def eq3(v, v0, a): # S = ((V + V0)/2)t
    return ((v + v0) / 2) * (v - v0) / a

"""
v = rw
"""

def eq4(r, v): # v= rw
    return v/r

def eq5(w, t): # w = dθ / dt
    return w * t
