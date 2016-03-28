#!/usr/bin/env python
# Author: Griswald Brooks

## @file arm_rotations.py Script for computing the arm rotations needed to 
## make the forearm of the Nao point forward.

import numpy as np
from numpy import sqrt, square, cos, sin, arccos, pi

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import linalg as la
# import matplotlib.animation as animation

def Rotate(k, theta, v):
	return v*cos(theta) + np.cross(k, v)*sin(theta) + k*np.dot(k, v)*(1 - cos(theta))

def computeElbowYawPK(nh, theta_er, vh, vf):
	vhw = Rotate(nh, theta_er, vh)
	vhnw = vhw - np.dot(vhw, vh)*vh
	vfnw = vf - np.dot(vf, vh)*vh

	return arccos(np.dot(vhnw, vfnw)/(la.norm(vhnw)*la.norm(vfnw)))

def computeElbowYaw(nh, vf, vh):
	# The direction vector needed that rotates vh onto vf.
	# u is the vector nh needs to be rotated to so vh can be
	# rotated onto vf.
	u = np.cross(vh, vf)
	u = u/la.norm(u) 
	# print('norm(u) = ' + str(la.norm(u)))

	# Compute the angle betwwen nh and u.
	return arccos(np.dot(nh, u))

def main():
	# The angle that the projected humerus makes with the x-axis.
	alpha = -pi/6

	# The distance from the shoulder to the elbow in the y-axis.
	d = 0.5
	# The length of the humerus.
	lh = 1.0
	# The length of the humerus projected onto the z-x plane.
	lhw = sqrt(square(lh) - square(d))

	# The direction the forearm is required to point.
	vf = np.array([1, 0, 0])
	print('norm(vf) = ' + str(la.norm(vf)))
	# The direction vector of the humerus, which is the axis of rotation of the elbow yaw.
	vh = np.array([lhw*cos(alpha), -d, lhw*sin(alpha)])/lh
	print('norm(vh) = ' + str(la.norm(vh)))
	# The direction vector of the axis of the elbow roll, when elbow yaw is zero.
	nh = np.array([-sin(alpha), 0, cos(alpha)])
	print('norm(nh) = ' + str(la.norm(nh)))

	# The amount to rotate vh to get to vf.
	theta_er = arccos(np.dot(vh, vf))

	# The amount to rotate the forearm around vh to align nh with u.
	theta_ey = computeElbowYaw(nh, vf, vh)
	# theta_ey = computeElbowYawPK(nh, theta_er, vh, vf)

	# The resultant vector after rotations.
	uf = Rotate(vh, theta_ey, Rotate(nh, theta_er, vh))
	print('norm(uf) = ' + str(la.norm(uf)))
	print(uf)

	# Set up plot.
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.set_aspect('equal')

	vf_legend, = plt.plot([0, vf[0]], [0, vf[1]], [0, vf[2]], 'b-', label='vf')
	vh_legend, = plt.plot([0, vh[0]], [0, vh[1]], [0, vh[2]], 'g-', label='vh')
	nh_legend, = plt.plot([0, nh[0]], [0, nh[1]], [0, nh[2]], 'm-', label='nh')
	# u_legend,  = plt.plot([0,  u[0]], [0,  u[1]], [0,  u[2]], 'y-', label='u')
	uf_legend, = plt.plot([0, uf[0]], [0, uf[1]], [0, uf[2]], 'r-', label='uf')
	
	# plt.legend([vf_legend, vh_legend, nh_legend, u_legend, uf_legend], ['vf', 'vh', 'nh', 'u', 'uf'])
	plt.legend([vf_legend, vh_legend, nh_legend, uf_legend], ['vf', 'vh', 'nh', 'uf'])
	ax.set_xlim3d(-2, 2)
	ax.set_ylim3d(-2, 2)
	ax.set_zlim3d(-2, 2)
	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')
	ax.legend()
	plt.show()

if __name__ == '__main__':
	main()