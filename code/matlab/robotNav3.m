%%% Robot Navigation Algorithm %%%
% Input:
%     ranges    A 1D arrary of scalar distance measurements
% Output:
%     v         Robot linear velocity in cm/sec
%     om        Robot angular velocity in radians/sec
function [v, om, poses, stuck_timer, rand_goal] = robotNav3(ranges, base_angle, r_pose, poses, stuck_timer, rand_goal, goal, vp, dt)

% Constants
plot_scaler = 1000;
OM_MAX = 1;
VAR_THRESH = 5;


% Calculate Occlusion Forces
f_ranges = OccForce3(ranges, base_angle + 20);

% Calculate Goal Force
goal_range = sqrt((r_pose(1) - goal(1))^2 + (r_pose(2) - goal(2))^2);
f_goal = (1/((0.5*min(goal_range,25000))^2))*[goal(1) - r_pose(1), goal(2) - r_pose(2)]';
f_goal = [cos(-r_pose(3)),-sin(-r_pose(3));sin(-r_pose(3)),cos(-r_pose(3))]*f_goal;

% Check for being Stuck
[stuck_timer, rand_goal] = CheckStuck(poses, VAR_THRESH, stuck_timer, rand_goal);

if((stuck_timer.time > 0) && (goal_range > 50))  
    goal = rand_goal;
    goal_range = sqrt((r_pose(1) - goal(1))^2 + (r_pose(2) - goal(2))^2);
    f_goal = (1/((0.5*min(goal_range,25000))^2))*[goal(1) - r_pose(1), goal(2) - r_pose(2)]';
    f_goal = [cos(-r_pose(3)),-sin(-r_pose(3));sin(-r_pose(3)),cos(-r_pose(3))]*f_goal;
    stuck_timer.time = stuck_timer.time - 1
    if(stuck_timer.time == 0)
        stuck_timer.stuck = 0;
    end
end

% Calculate Inertia
f_heading = 0.01*[cos(0),sin(0)]';

% Sum Forces
f = f_ranges + f_goal + f_heading;




% Calculate Angular Velocity
th_in = (atan2(f(2),f(1)));
TURN_MAGNITUDE = 0.8;
om = TURN_MAGNITUDE*th_in*dt;

% Calculate Linear Velocity
v_desired = 0.75*log(min(ranges)/30)*(5*exp(-om));
v = 0.1*vp + 0.9*v_desired;

% Angular Saturation
if(om > OM_MAX)
    om = OM_MAX;
elseif (om < -OM_MAX)
    om = -OM_MAX;
end

% Stop at goal
if(goal_range < 10)
    v = 0;
    om = 0;
end

% Plot Forces
plotForce(f_ranges, r_pose, plot_scaler, 'g');
plotForce(f_goal, r_pose, plot_scaler, 'm');
plotForce(f_heading, r_pose, plot_scaler, 'k');
plotForce(f, r_pose, plot_scaler, 'b');


% In Graph Text
text(10,6,'om: ');
text(70, 6, num2str(om));

% Update Poses
poses = updatePoses(poses, v, om, dt);

