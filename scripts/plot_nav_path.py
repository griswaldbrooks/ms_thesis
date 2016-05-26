#!/usr/bin/env python
#
# Software Licence Agreement (MIT)
#
# Copyright (c) 2016 Griswald Brooks
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

##
# @author Griswald Brooks

## @file plot_nav_path.py Script for plotting path positions from file.

import numpy as np
import argparse
import matplotlib.pyplot as plt


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('poly_points', metavar='best-fit-line-points',
                        help='Points representing the best fit line for the sample points.')
    parser.add_argument('sample_set', metavar='sample-points',
                        help='Points sampled from the video to generate path.')
    parser.add_argument('figure_title', metavar='figure-title', nargs='?',
                        help='Title for the figure.')
    parser.add_argument('output_filename', metavar='output-filename', nargs='?',
                        help='Name to use when saving the figure.')
    args = parser.parse_args()

    # Load  data.
    poly_points = np.loadtxt(args.poly_points, delimiter=',')
    sample_points = np.loadtxt(args.sample_set, delimiter=',')

    start = np.array([])
    goal = np.array([])

    # Narrow Area Path Endpoints
    # start = np.array([64.0, 61.0])
    # goal = np.array([570.0, 65.0])

    # Open Area Path Endpoints
    # start = np.array([35.0, 54.0])
    # goal = np.array([578.0, 243.0])

    # Square Area Path Endpoints
    # start = np.array([67.0, 72.0])
    # goal = np.array([622.0, 74.0])

    # Scale data.
    poly_points /= 58.0  # Pixels per foot.
    sample_points /= 58.0

    poly_points *= 0.305  # Meters per foot.
    sample_points *= 0.305

    if start.size is not 0:
        # Scale data.
        start /= 58.0  # Pixels per foot.
        goal /= 58.0
        start *= 0.305  # Meters per foot.
        goal *= 0.305

    # Plot result
    plt.plot(poly_points[:, 0], poly_points[:, 1], '-', color='g',
             linewidth=3, label='Best Fit Path')

    plt.plot(sample_points[:, 0], sample_points[:, 1], 'o', markerfacecolor='b',
             markeredgecolor='k', markersize=2, label='Samples Extracted From Video')

    if start.size is not 0:
        plt.plot(start[0], start[1], 's', color='r', markeredgecolor='k', markersize=10, label='Start Location')
        plt.plot(goal[0], goal[1], '*', color='y', markeredgecolor='k', markersize=10, label='Goal Location')

    plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)

    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.margins(0.1)
    plt.xlabel('Distance (meters)')
    plt.ylabel('Distance (meters)')
    plt.grid(True)
    if args.figure_title is not None:
        plt.title(args.figure_title)
    else:
        plt.title('Navigation Path')
    if args.output_filename is not None:
        plt.savefig(args.output_filename + '.png', dpi=300, format='png')
    else:
        plt.savefig('nav_figure.png', dpi=300, format='png')
    plt.show()

if __name__ == '__main__':
    main()
