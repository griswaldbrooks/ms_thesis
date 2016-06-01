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
# from matplotlib import cm
from matplotlib import colors
from os import path
import yaml


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


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

    # Plot torques on a per duration basis.
    for nom_torque, nom_duration in zip(nom_torques, nom_durations):
        nom_fig, nom_axis = plt.subplots()

        # Generate times.
        t = np.linspace(0.0, nom_duration, len(nom_torque))

        # Add curve to plot.
        nom_axis.plot(t, nom_torque[:, 0], color='r', linewidth=2, label='Joint ' + r'$\theta_2$')
        nom_axis.plot(t, nom_torque[:, 1], color='g', linewidth=2, label='Joint ' + r'$\theta_3$')
        nom_axis.plot(t, nom_torque[:, 2], color='b', linewidth=2, label='Joint ' + r'$\theta_4$')
        nom_axis.plot(t, nom_torque[:, 3], color='m', linewidth=2, label='Joint ' + r'$\theta_5$')
        nom_axis.set_title('Nominal Gait: ' + str(nom_duration) + ' second duration')
        nom_axis.margins(0.1)
        nom_axis.set_ylabel('Torque (N/m)')
        nom_axis.set_xlabel('Time (seconds)')
        nom_axis.grid(True)
        plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
        nom_fig.savefig('nom_torques_duration_' + str(nom_duration) + '_1.png', dpi=300, format='png')

    for opt_torque, opt_duration in zip(opt_torques, opt_durations):
        opt_fig, opt_axis = plt.subplots()

        # Generate times.
        t = np.linspace(0.0, opt_duration, len(opt_torque))

        # Add curve to plot.
        opt_axis.plot(t, opt_torque[:, 0], color='r', linewidth=2, label='Joint ' + r'$\theta_2$')
        opt_axis.plot(t, opt_torque[:, 1], color='g', linewidth=2, label='Joint ' + r'$\theta_3$')
        opt_axis.plot(t, opt_torque[:, 2], color='b', linewidth=2, label='Joint ' + r'$\theta_4$')
        opt_axis.plot(t, opt_torque[:, 3], color='m', linewidth=2, label='Joint ' + r'$\theta_5$')
        opt_axis.set_title('Optimal Gait: ' + str(opt_duration) + ' second duration')
        opt_axis.margins(0.1)
        opt_axis.set_ylabel('Torque (N/m)')
        opt_axis.set_xlabel('Time (seconds)')
        opt_axis.grid(True)
        plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
        opt_fig.savefig('opt_torques_duration_' + str(opt_duration) + '_1.png', dpi=300, format='png')

    # Plot torques on a per joint basis.
    for joint_ndx in range(0, 4):
        # Generate colormap for figures.
        nom_cm = truncate_colormap(plt.get_cmap('Reds'), 0.5, 1.0)
        opt_cm = truncate_colormap(plt.get_cmap('Blues'), 0.5, 1.0)
        # Get fresh plots.
        jt_fig, jt_axis = plt.subplots()

        # Iterate through torque sets and pull off appropriate joint.
        for opt_tor, nom_tor, dur in zip(opt_torques, nom_torques, nom_durations):

            # Generate times.
            t = np.linspace(0.0, 100.0, len(nom_tor))
            # Get color value.
            dur_range = [min(nom_durations), max(nom_durations)]
            color_range = [0.0, 1.0]
            color_value = np.interp(dur, dur_range, color_range)
            # Add curve to plot.
            jt_axis.plot(t, nom_tor[:, joint_ndx], c=nom_cm(color_value),
                         linewidth=2, linestyle='-', label='Nominal')
            jt_axis.plot(t, opt_tor[:, joint_ndx], c=opt_cm(color_value),
                         linewidth=2, linestyle='--', label='Optimal')

        # Set plot parameters for whole figure.
        jt_axis.set_title('Joint ' + r'$\theta_' + str(joint_ndx + 2) + '$')
        jt_axis.margins(0.1)
        jt_axis.set_ylabel('Torque (N/m)')
        jt_axis.set_xlabel('Percentage of Gait Cycle (%)')
        jt_axis.grid(True)

        # Set colorbars for nominal and optimal gaits.
        sm = plt.cm.ScalarMappable(cmap=nom_cm, norm=plt.Normalize(vmin=1, vmax=10))
        sm._A = []
        jt_colorbar = jt_fig.colorbar(sm, shrink=0.9, pad=0.0)
        jt_colorbar.set_label('Duration of Nominal Gait (Seconds)')

        sm = plt.cm.ScalarMappable(cmap=opt_cm, norm=plt.Normalize(vmin=1, vmax=10))
        sm._A = []
        jt_colorbar = jt_fig.colorbar(sm, shrink=0.9, pad=0.02)
        jt_colorbar.set_label('Duration of Optimized Gait (Seconds)')

        # Save figure.
        jt_fig.savefig('joint' + str(joint_ndx + 2) + '_torques' + '.png', dpi=300, format='png')

    # Compute costs and improvements.
    nom_costs = []
    opt_costs = []

    for torque in nom_torques:
        sq_tor = np.square(torque)
        # weight = np.array([1, 1, 1, 5])
        weight = np.array([1, 1, 1, 1])
        cost = np.sum(np.sum(weight*sq_tor))
        nom_costs.append(cost)

    for torque in opt_torques:
        sq_tor = np.square(torque)
        # weight = np.array([1, 1, 1, 5])
        weight = np.array([1, 1, 1, 1])
        cost = np.sum(np.sum(weight*sq_tor))
        opt_costs.append(cost)

    # Plot costs.
    fig, ax = plt.subplots()
    times = np.linspace(min(nom_durations), max(nom_durations), len(nom_durations))
    ax.plot(times, nom_costs, '-', color='g', linewidth=3, label='Nominal')
    ax.plot(times, opt_costs, '--', color='r', linewidth=3, label='Optimal')
    ax.set_title('Gait Cost vs Duration')
    ax.margins(0.1)
    ax.set_xlabel('Gait Duration (seconds)')
    ax.set_ylabel('Cost (' + r'$\frac{N^2}{m^2}$' + ')')
    ax.grid(True)
    plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
    fig.savefig('gait_cost_duration1.png', dpi=300, format='png')
    np.savetxt('gait_costs_nominal1.txt', np.transpose(nom_costs), delimiter=',')
    np.savetxt('gait_costs_optimal1.txt', np.transpose(opt_costs), delimiter=',')

    # Plot improvements.
    fig, ax = plt.subplots()
    times = np.linspace(min(nom_durations), max(nom_durations), len(nom_durations))
    ax.plot(times, np.asarray(opt_costs)/np.asarray(nom_costs), color='b', linewidth=3)
    ax.set_title('Cost Improvements vs. Gait Duration')
    ax.margins(0.1)
    ax.set_xlabel('Gait Duration (seconds)')
    ax.set_ylabel('Percentage of Original Cost (%)')
    ax.grid(True)
    fig.savefig('cost_imp_duration1.png', dpi=300, format='png')

    plt.show()

if __name__ == '__main__':
    main()
