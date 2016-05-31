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

## @file plot_vrep_torques.py Script for plotting the torques found from running the
##                            projected profile crawl gait on the V-REP Nao.

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from os import path
import yaml


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('torque_yaml', metavar='torque-yaml',
                        help='Yaml file containing the list of torque files and their associated folders.')
    args = parser.parse_args()

    # Load torque data metadata.
    with open(args.torque_yaml, 'r') as f:
        torque_doc = yaml.load(f)

    # Load torque data.
    nom_torques = []
    opt_torques = []
    torque_dir = path.dirname(args.torque_yaml)
    nom_dir = torque_doc['nominal_files']['folder']
    opt_dir = torque_doc['optimal_files']['folder']

    for nom_file in torque_doc['nominal_files']['files']:
        nom_torques.append(np.loadtxt(torque_dir + '/' + nom_dir + '/' + nom_file, delimiter=','))

    for opt_file in torque_doc['optimal_files']['files']:
        opt_torques.append(np.loadtxt(torque_dir + '/' + opt_dir + '/' + opt_file, delimiter=','))

    nom_durations = np.array(torque_doc['nominal_files']['durations'])
    opt_durations = np.array(torque_doc['optimal_files']['durations'])

    # Plot torques.
    # f, nom_axes = plt.subplots(4, 2, sharex=True, sharey=True)
    # nom_axes = [axis for axis_set in nom_axes for axis in axis_set]
    # for nom_torque, duration, nom_axis in zip(nom_torques, nom_durations, nom_axes):
    #     # Generate times.
    #     t = np.linspace(0.0, 1.0, len(nom_torque))
    #     # Add curve to plot.
    #     nom_axis.plot(t, nom_torque[:, 0], color='r')
    #     nom_axis.plot(t, nom_torque[:, 1], color='g')
    #     nom_axis.plot(t, nom_torque[:, 2], color='b')
    #     nom_axis.plot(t, nom_torque[:, 3], color='m')
    #     nom_axis.set_title(str(duration))
    #     nom_axis.margins(0.1)

    # f, opt_axes = plt.subplots(4, 2, sharex=True, sharey=True)
    # opt_axes = [axis for axis_set in opt_axes for axis in axis_set]
    # for torque, duration, axis in zip(opt_torques, opt_durations, opt_axes):
    #     # Generate times.
    #     t = np.linspace(0.0, 1.0, len(torque))
    #     # Add curve to plot.
    #     axis.plot(t, torque[:, 0], color='r')
    #     axis.plot(t, torque[:, 1], color='g')
    #     axis.plot(t, torque[:, 2], color='b')
    #     axis.plot(t, torque[:, 3], color='m')
    #     axis.set_title(str(duration))
    #     axis.margins(0.1)

    # Plot torques on a per joint basis.
    # f, jt_axes = plt.subplots(2, 2, sharex=True, sharey=True)
    # jt_axes = [axis for axis_set in jt_axes for axis in axis_set]
    # for jt_axis, joint_ndx in zip(jt_axes, range(0, 4)):
    for joint_ndx in range(0, 4):
        f, jt_axis = plt.subplots()
        # Iterate through torque sets and pull off appropriate joint.
        for opt_tor, nom_tor, dur in zip(opt_torques, nom_torques, nom_durations):

            # Generate times.
            t = np.linspace(0.0, 1.0, len(nom_tor))
            # Add curve to plot.
            jt_axis.plot(t, nom_tor[:, joint_ndx], c=cm.Reds(dur/10.0), linewidth=2, linestyle='-')
            jt_axis.plot(t, opt_tor[:, joint_ndx], c=cm.Blues(dur/10.0), linewidth=2, linestyle='--')

        jt_axis.set_title(str(joint_ndx))
        jt_axis.margins(0.1)

    # f, opt_axes = plt.subplots(4, 2, sharex=True, sharey=True)
    # opt_axes = [axis for axis_set in opt_axes for axis in axis_set]
    # for torque, duration, axis in zip(opt_torques, opt_durations, opt_axes):
    #     # Generate times.
    #     t = np.linspace(0.0, 1.0, len(torque))
    #     # Add curve to plot.
    #     axis.plot(t, torque[:, 0], color='r')
    #     axis.plot(t, torque[:, 1], color='g')
    #     axis.plot(t, torque[:, 2], color='b')
    #     axis.plot(t, torque[:, 3], color='m')
    #     axis.set_title(str(duration))
    #     axis.margins(0.1)

    # Compute costs and improvements.
    nom_costs = []
    opt_costs = []

    for torque in nom_torques:
        sq_tor = np.square(torque)
        weight = np.array([1, 1, 1, 5])
        cost = np.sum(np.sum(weight*sq_tor))
        nom_costs.append(cost)

    for torque in opt_torques:
        sq_tor = np.square(torque)
        weight = np.array([1, 1, 1, 5])
        cost = np.sum(np.sum(weight*sq_tor))
        opt_costs.append(cost)

    # Plot costs.
    f, ax = plt.subplots()
    times = np.linspace(min(nom_durations), max(nom_durations), len(nom_durations))
    ax.plot(times, nom_costs, color='g')
    ax.plot(times, opt_costs, color='r', linewidth=4)
    ax.set_title('Gait Costs')
    ax.margins(0.1)
    ax.set_xlabel('Gait Duration (seconds)')
    ax.set_ylabel('Cost')

    # Plot improvements.
    f, ax = plt.subplots()
    times = np.linspace(min(nom_durations), max(nom_durations), len(nom_durations))
    ax.plot(times, np.asarray(opt_costs)/np.asarray(nom_costs), color='b')
    ax.set_title('Reduction of Cost')
    ax.margins(0.1)
    ax.set_xlabel('Gait Duration (seconds)')
    ax.set_ylabel('Percent of Original Cost')

    # plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)

    # plt.axis('equal')
    # plt.margins(0.1)
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Torque (N/m)')
    # plt.grid(True)
    # if args.figure_title is not None:
    #     plt.title(args.figure_title)
    # else:
    #     plt.title('Navigation Path')
    # if args.output_filename is not None:
    #     plt.savefig(args.output_filename + '.png', dpi=300, format='png')
    # else:
    #     plt.savefig('nav_figure.png', dpi=300, format='png')
    plt.show()

if __name__ == '__main__':
    main()
