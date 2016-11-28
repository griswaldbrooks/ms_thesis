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


def generate_field(xmin, xmax, xstep, ymin, ymax, ystep):
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
    X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2),
                       np.arange(0, 2 * np.pi, .2))
    # Generate outputs.
    U = np.cos(X)
    V = np.sin(Y)

    # Block out obstacles.
    M = np.zeros(U.shape, dtype='bool')
    M[U.shape[0]//3:2*U.shape[0]//3,
      U.shape[1]//3:2*U.shape[1]//3] = True
    U = ma.masked_array(U, mask=M)
    V = ma.masked_array(V, mask=M)

    return X, Y, U, V


def plot_field(X, Y, U, V):
    '''
    Function to plot the potential field.

    Args:
        X (numpy.ndarray): X component of the sample points.
        Y (numpy.ndarray): Y component of the sample points.
        U (numpy.ndarray): X component of field at sample points.
        V (numpy.ndarray): Y component of field at sample points.
    '''
    # Generate plot.
    plt.figure()
    Q = plt.quiver(X[::3, ::3], Y[::3, ::3], U[::3, ::3], V[::3, ::3],
                   color='b',
                   units='x',
                   pivot='tip')
    plt.quiverkey(Q, 0.9, 1.05, 1, r'$1 \frac{m}{s}$',
                  labelpos='E',
                  fontproperties={'weight': 'bold'})
    plt.axis([-1, 7, -1, 7])
    plt.title("scales with x view; pivot='tip'")

    plt.show()


def main():
    '''
    Function to generate potential fields plot from a map.
    '''

    [X, Y, U, V] = generate_field(0, 0, 0, 0, 0, 0)
    plot_field(X, Y, U, V)


if __name__ == '__main__':
    main()
