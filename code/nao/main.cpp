#include <iostream>
#include <alerror/alerror.h>
#include <alproxies/almotionproxy.h>
#include <alproxies/dcmproxy.h>
#include <alproxies/almemoryproxy.h>
#include <alproxies/alsonarproxy.h>
#include <alproxies/alsensorsproxy.h>
#include <alproxies/alredballtrackerproxy.h>
#include <qi/os.hpp>
#include <math.h>
#include <time.h>

#include "robotNav.h"

bool robotHalted = false;
double time_from_start = 0;

int main(int argc, char* argv[]) {
	if(argc != 2){
		std::cerr << "Wrong number of arguments!" << std::endl;
		std::cerr << "Usage: RApath NAO_IP" << std::endl;
		exit(2);
	}
	
	// Initialize Sonar and Memory Proxies to start Sonar
	// Hardware and retrieve data
	AL::ALSonarProxy sonarPrx(argv[1], 9559);
	AL::ALMemoryProxy memPrxSonar(argv[1], 9559);

	sonarPrx.subscribe("RAPlanner");
	int period = sonarPrx.getMyPeriod("RAPlanner");

	// Initialize Bumper and Memory Proxies
	AL::ALSensorsProxy headTouchPrx(argv[1], 9559);
	AL::ALMemoryProxy memPrxBumper(argv[1], 9559);

	headTouchPrx.subscribe("RAPlanner");
	float headTouched = memPrxBumper.getData("FrontTactilTouched");

	// Values to store current distance measurements
	AL::ALValue rightDist, leftDist;
	float rightD, leftD;
	// Sonar Value keystrings (locations in memory)
	const std::string keyR = "Device/SubDeviceList/US/Right/Sensor/Value";
	const std::string keyL = "Device/SubDeviceList/US/Left/Sensor/Value";

	// Initialize Motion Proxy
	AL::ALMotionProxy motionPrx(argv[1], 9559);
	// Walk Velocity Variables
	float Vx = 0;
	float Vy = 0;
	float Om = 0;
	float stepFreq = 1;

	// Pose
	bool useSensorValues = true;
	std::vector<float> pose = motionPrx.getRobotPosition(useSensorValues);
	std::vector<float> headAngle = motionPrx.getAngles("HeadYaw", true);

	// Set Head
	motionPrx.setStiffnesses("Head", 1.0f);
	motionPrx.setAngles("HeadYaw", 0.0f, 0.2f);
	motionPrx.setAngles("HeadPitch", 0.0f, 0.2f);
	

	// Initialize Red Ball Tracker
	AL::ALRedBallTrackerProxy redBallPrx(argv[1], 9559);
	redBallPrx.startTracker();
	std::vector<float> ballPose;
	float ballMag = 1000.0f;
	int ballCounter = 0;
	ballPose.push_back(1000.0f);
	ballPose.push_back(0.0f);
	ballPose.push_back(0.0f);
	
	// Initialize Walk
	motionPrx.walkInit();
	motionPrx.setWalkTargetVelocity(Vx, Vy, Om, stepFreq);

	// File Processing
	FILE* fh = fopen("sonarLog1.txt", "w");
	
	AL::DCMProxy dcm_proxy(argv[1], 9559);
	
	int t1 = dcm_proxy.getTime(0);			
	try {
		std::cout << "Test" << std::endl;
		// Poll Sonars
		while(true){
			// Head Pressed?
			headTouched = memPrxBumper.getData("FrontTactilTouched");
			if(headTouched) robotHalted = true;

			if(!robotHalted){
				int t2 = dcm_proxy.getTime(0);			
				time_from_start = (t2-t1)/1000.0;
				// Update Ball Pose
				if(redBallPrx.isNewData()){
					ballPose = redBallPrx.getPosition();
					// Convert to Centimeters
					ballPose[0] *= 100;
					ballPose[1] *= 100;
					ballPose[2] *= 100;

					ballMag = sqrt(pow(ballPose[0],2) + pow(ballPose[1],2));
				}
				else{
					motionPrx.setAngles("HeadYaw", 0.0f, 0.2f);
					motionPrx.setAngles("HeadPitch", 0.0f, 0.2f);
				}
				// Get Distances
				rightDist = memPrxSonar.getData(keyR);
				leftDist = memPrxSonar.getData(keyL);
				// Convert to Centimeters
				rightD = 100*float(rightDist);
				leftD  = 100*float(leftDist);

				robotNav(ballPose, Om, Vx, rightD, leftD);
		
				if(ballMag < 30.0f){
					if(ballCounter > 15){
						Vx = 0;
						Om = 0;
						robotHalted = true;
						std::cout << std::endl << " GOAL REACHED " << std::endl;
					}
					ballCounter++;
					std::cout << " Ball Counter: " << ballCounter;
				}

				// Constrain velocities
				if(Vx < -1.0f) Vx = -1.0f;
				if(Vx > 1.0f) Vx = 1.0f;
				if(Om < -1.0f) Om = -1.0f;
				if(Om > 1.0f) Om = 1.0f;
			
				// Update Walk
				motionPrx.setWalkTargetVelocity(Vx, Vy, Om, stepFreq);

				// Update Pose
				pose = motionPrx.getRobotPosition(useSensorValues);

				// Get Head Yaw
				headAngle = motionPrx.getAngles("HeadYaw", true);

				// Print Values
				std::cout << " LDist: " << leftD;
				std::cout << " RDist: " << rightD;
				//std::cout << " Vx: " << Vx << " Om: " << Om;
				//std::cout << " Period (ms): ";
				//std::cout << " Pose: " << pose;
				//std::cout << " Ball Pose ";
				//std::cout << " x: " << ballPose[0];
				//std::cout << " y: " << ballPose[1];
				//std::cout << " z: " << ballPose[2];
				std::cout << std::endl;
				
				// Log sonar data
				fprintf(fh, "%lf %lf %lf %lf %lf %lf\n", time_from_start, leftD, rightD, headAngle, ballPose[0],ballPose[1],ballPose[2]);

			}
			else{
				std::cout << "Robot Halted." << std::endl;
				motionPrx.setWalkTargetVelocity(0.0f, 0.0f, 0.0f, 0.0f);
				redBallPrx.stopTracker();
				motionPrx.setStiffnesses("Head", 0.0f);
				qi::os::sleep(30);
				fclose(fh);
			}
		}

	}
	catch (const AL::ALError& e) {
		motionPrx.setWalkTargetVelocity(0.0f, 0.0f, 0.0f, 0.0f);
	    std::cerr << "Caught exception: " << e.what() << std::endl;
		exit(1);
	}
	exit(0);
}
