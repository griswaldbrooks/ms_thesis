#include "robotNav.h"

void robotNav(std::vector<float> &goal_pose, float &Om, float &V, float rightD, float leftD){

	// Constants
	float plot_scaler = 1000;
	float OM_MAX = 1;
	float sub_angle = 15.0*(M_PI/180);
	float VAR_THRESH = 5;
	float base_angle = 45.0*(M_PI/180);

	// Memory
	static float Vp = 0;
	static float Omp = 0;
	static double prev_time = 0;

	// Calculate Goal Force
	float goal_range = sqrt(pow(goal_pose[0],2) + pow(goal_pose[1],2));
	Force f_goal;
	float goalCoeff = 250*(0.0001+pow(goal_range,-2.2f)+0.03*pow(goal_range,-1.0f));

	f_goal.x = goalCoeff*(goal_pose[0]);
	f_goal.y = goalCoeff*(goal_pose[1]);

	//if (0)
	//{
	//std::cout << " Goal Vector ";
	//std::cout << " mag: " << goalCoeff;
	//std::cout << " ang: " << atan2(f_goal.y, f_goal.x);
	//}
	//std::cout << std::endl;

	// Calculate Occlusion Forces
	Force f_ranges = OccForce(rightD, leftD, base_angle, sub_angle, goal_range);

	// Calculate Inertia
	Force f_heading;
	f_heading.x = 0.01*cos(0.0);
	f_heading.y = 0.01*sin(0.0);

	// Sum Forces
	Force f;
	f.x = f_ranges.x + f_goal.x + f_heading.x;
	f.y = f_ranges.y + f_goal.y + f_heading.y;
	
	//std::cout << " Force Vector ";
	//std::cout << " mag: " << sqrt(pow(f.y,2) + pow(f.x,2));
	//std::cout << " ang: " << atan2(f.y, f.x);
	//std::cout << std::endl;

	// Calculate Angular Velocity
	Om = 4.0*atan2(f.y,f.x)*dt;

	// Calculate Linear Velocity
	float Vd = 0.4*log(1+0.2*std::min(leftD, rightD)/30)*(5*exp(-Om));
	V = 0.1*Vp + 0.9*Vd;

	Vp = V;
	Omp = Om;

}

Force OccForce(float rightD, float leftD, float base_angle, float sub_angle, float goal_range){
	float RANGE_OFF = 15.0;
	float RANGE_COEFF = -2400;
	if (goal_range < 75) RANGE_COEFF *= (goal_range/75.);
	double d_left = leftD_deriv->d , d_right = rightD_deriv->d;

	float rightCoeff = RANGE_COEFF*(pow((rightD - RANGE_OFF),-2)+0.15*pow((rightD - RANGE_OFF),-1.0f));
	float leftCoeff =  RANGE_COEFF*(pow((leftD - RANGE_OFF),-2)+0.15*pow((leftD - RANGE_OFF),-1.0f));

	Force f_range1, f_range2, f_ranges;

	// Right Sensor
	f_range1.x = rightCoeff*cos(-base_angle);
	f_range1.y = rightCoeff*sin(-base_angle);

	// Left Sensor
	f_range2.x = leftCoeff*cos(base_angle);
	f_range2.y = leftCoeff*sin(base_angle);

	f_ranges.x = f_range1.x + f_range2.x;
	f_ranges.y = f_range1.y + f_range2.y;

	return f_ranges;
}

bool stuck(float V){
	std::deque<float> pLinVels;
	float sum = 0;
	float avg = 0;
	// Keep a sliding window of velocities
	pLinVels.push_back(V);
	if(pLinVels.size() > 100) pLinVels.pop_front();

	// Take average
	for(size_t ndx = 0; ndx < pLinVels.size(); ndx++){
		sum += pLinVels[ndx];
	}
	avg = sum/pLinVels.size();

	if(avg < 0.2) return true;

	return false;
}