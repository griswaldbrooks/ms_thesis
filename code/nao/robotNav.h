#ifndef _ROBOT_NAV_H
#define _ROBOT_NAV_H

#include <math.h>
#include <vector>
#include <deque>
#include <iostream>

#define M_PI 3.14159265359

class Force{
public:
	float x;
	float y;
};


void robotNav(std::vector<float> &pose, float &Om, float &V, float rightD, float leftD);

Force OccForce(float rightD, float leftD, float base_angle, float sub_angle, float goal_range);

bool stuck(float V);

#endif