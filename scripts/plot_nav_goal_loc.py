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

## @file plot_nav_goal_loc.py Script for plotting the nav goal locations from file.

import numpy as np
import argparse
import matplotlib.pyplot as plt


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('nav_goal_log', metavar='navigation-goal-log',
                        help='Log of commands and goal locations from Nao.')
    parser.add_argument('figure_title', metavar='figure-title', nargs='?',
                        help='Title for the figure.')
    parser.add_argument('output_filename', metavar='output-filename', nargs='?',
                        help='Name to use when saving the figure.')
    args = parser.parse_args()

    # Load  data.
    nav_log = np.loadtxt(args.nav_goal_log, delimiter=',')

    # Find first index.
    first_ndx = 0
    zero_indices, = np.where(nav_log[:, 3] == 0.0)
    if zero_indices.size is not 0:
        first_ndx = np.max(zero_indices) + 1

    # Plot result
    # Range nav_log[:, 3]
    # Angle nav_log[:, 4]
    plt.plot(nav_log[first_ndx:, 0], nav_log[first_ndx:, 3], 'o-', markerfacecolor='b',
             markeredgecolor='k', markersize=4, linewidth=2, label='Range to Goal')
    plt.plot(nav_log[first_ndx:, 0], nav_log[first_ndx:, 4], 'o-', markerfacecolor='g',
             markeredgecolor='k', markersize=4, linewidth=2, label='Bearing to Goal')

    plt.legend(loc='upper right', shadow=True, fontsize='large')

    plt.xlabel('Time (Seconds)')
    plt.ylabel('Range/Bearing (meters/radians)')
    plt.grid(True)

    # Set the figure title.
    fig_title = 'Ranges and Bearings'

    if args.figure_title is not None:
        fig_title = args.figure_title

    plt.title(fig_title)

    # Save the figure.
    fig_filename = 'nav_ranges_and_bearings.png'

    if args.output_filename is not None:
        fig_filename = args.output_filename + '.png'

    plt.savefig(fig_filename, dpi=300, format='png')

    plt.show()

if __name__ == '__main__':
    main()
