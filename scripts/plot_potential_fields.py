#!/usr/bin/env python
#
# Software Licence Agreement (MIT)
#
# Copyright (c) 2016 Griswald Brooks
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

##
# @author Griswald Brooks

# @file plot_potential_fields.py Script for plotting potential fields.
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma


def get_goal():
    return 1.5, 5.


def generate_field_navtrap_map(xmin, xmax, xstep, ymin, ymax, ystep):
    '''
    Function to generate the potential field.

    Args:
        xmin  (float): Minimum x value of the sample space.
        xmax  (float): Maximum x value of the sample space.
        xstep (float): Sampling interval along the x dimension.
        ymin  (float): Minimum y value of the sample space.
        ymax  (float): Maximum y value of the sample space.
        ystep (float): Sampling interval along the y dimension.

    Returns:
        (tuple): tuple containing:
            X (numpy.ndarray): X component of the sample points.
            Y (numpy.ndarray): Y component of the sample points.
            U (numpy.ndarray): X component of field at sample points.
            V (numpy.ndarray): Y component of field at sample points.
    '''
    # Generate sample points.
    x = np.arange(xmin, xmax, xstep)
    y = np.arange(ymin, ymax, ystep)
    X, Y = np.meshgrid(x, y)
    # Create mask.
    M = np.zeros(X.shape, dtype='bool')

    # ## Generate outputs. ## #
    # Add goal.
    gx, gy = get_goal()
    GX = np.full_like(X, gx)
    GY = np.full_like(Y, gy)
    RG = np.sqrt(np.square(GX - X) + np.square(GY - Y))
    RG = np.clip(RG, 0.1, 10.)
    TG = np.arctan2(GY - Y, GX - X)

    U = 2. * np.reciprocal(RG) * np.cos(TG)
    V = 2. * np.reciprocal(RG) * np.sin(TG)

    # Block goal.
    M[gy//ystep, gx//xstep] = True

    rep_gain = -0.05

    # Add obstacle.
    bx, by = (11., 7.5)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (10.5, 6.875)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (10., 6.25)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (9.5, 5.625)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (9., 5.)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (9.5, 4.375)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (10., 3.75)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (10.5, 3.125)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True
    # Add obstacle.
    bx, by = (11., 2.5)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True

    # Clip vectors.
    RR = np.sqrt(np.square(U) + np.square(V))
    RR = np.clip(RR, 0., 0.2)
    TT = np.arctan2(V, U)
    U = RR * np.cos(TT)
    V = RR * np.sin(TT)

    # Block out items.
    U = ma.masked_array(U, mask=M)
    V = ma.masked_array(V, mask=M)

    return X, Y, U, V


def generate_field_potential_map(xmin, xmax, xstep, ymin, ymax, ystep):
    '''
    Function to generate the potential field.

    Args:
        xmin  (float): Minimum x value of the sample space.
        xmax  (float): Maximum x value of the sample space.
        xstep (float): Sampling interval along the x dimension.
        ymin  (float): Minimum y value of the sample space.
        ymax  (float): Maximum y value of the sample space.
        ystep (float): Sampling interval along the y dimension.

    Returns:
        (tuple): tuple containing:
            X (numpy.ndarray): X component of the sample points.
            Y (numpy.ndarray): Y component of the sample points.
            U (numpy.ndarray): X component of field at sample points.
            V (numpy.ndarray): Y component of field at sample points.
    '''
    # Generate sample points.
    x = np.arange(xmin, xmax, xstep)
    y = np.arange(ymin, ymax, ystep)
    X, Y = np.meshgrid(x, y)
    # Create mask.
    M = np.zeros(X.shape, dtype='bool')

    # ## Generate outputs. ## #
    # Add goal.
    gx, gy = get_goal()
    GX = np.full_like(X, gx)
    GY = np.full_like(Y, gy)
    RG = np.sqrt(np.square(GX - X) + np.square(GY - Y))
    RG = np.clip(RG, 0.1, 10.)
    TG = np.arctan2(GY - Y, GX - X)

    U = 2. * np.reciprocal(RG) * np.cos(TG)
    V = 2. * np.reciprocal(RG) * np.sin(TG)

    # Block goal.
    M[gy//ystep, gx//xstep] = True

    rep_gain = -0.2

    # Add obstacle.
    bx, by = (5., 6.)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True

    # Add obstacle.
    bx, by = (10., 3.)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True

    # Add obstacle.
    bx, by = (15., 4.)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True

    # Add obstacle.
    bx, by = (15., 5.)
    BX = np.full_like(X, bx)
    BY = np.full_like(Y, by)
    RB = np.sqrt(np.square(BX - X) + np.square(BY - Y))
    RB = np.clip(RB, 0.1, 10.)
    TB = np.arctan2(BY - Y, BX - X)

    U += rep_gain * np.reciprocal(RB) * np.cos(TB)
    V += rep_gain * np.reciprocal(RB) * np.sin(TB)
    M[by//ystep - 1:by//ystep + 1,
      bx//xstep - 1:bx//xstep + 1] = True

    # Clip vectors.
    RR = np.sqrt(np.square(U) + np.square(V))
    RR = np.clip(RR, 0., 0.2)
    TT = np.arctan2(V, U)
    U = RR * np.cos(TT)
    V = RR * np.sin(TT)

    # Block out items.
    U = ma.masked_array(U, mask=M)
    V = ma.masked_array(V, mask=M)

    return X, Y, U, V


def plot_field(X, Y, U, V, filename):
    '''
    Function to plot the potential field.

    Args:
        X (numpy.ndarray): X component of the sample points.
        Y (numpy.ndarray): Y component of the sample points.
        U (numpy.ndarray): X component of field at sample points.
        V (numpy.ndarray): Y component of field at sample points.
    '''
    # Generate plot.
    padding = 0.5
    plt.figure()
    plt.quiver(X, Y, U, V,
               color='#007ce8',
               units='x',
               pivot='tail')
    plt.axis('equal')
    plt.axis([np.amin(X) - padding,
              np.amax(X) + padding,
              np.amin(Y) - padding,
              np.amax(Y) + padding])
    # plt.savefig("potential_field_back1.svg", format='svg')
    plt.savefig(filename + ".svg", format='svg')
    plt.show()


def main():
    '''
    Function to generate potential fields plot from a map.
    '''

    # Potential fields.
    # [X, Y, U, V] = generate_field_potential_map(0, 25, 0.5, 0, 10, 0.5)
    # plot_field(X, Y, U, V, "potential_field_back1")
    # Nav trap.
    [X, Y, U, V] = generate_field_navtrap_map(0, 25, 0.5, 0, 10, 0.5)
    plot_field(X, Y, U, V, "navtrap_back1")


if __name__ == '__main__':
    main()
