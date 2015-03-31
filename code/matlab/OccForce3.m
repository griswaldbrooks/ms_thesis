function f_ranges = OccForce(ranges, base_angle)
RANGE_OFF = 20;
RANGE_COEFF = 0.1;

% Right Sensor
f_range1 = -1/(RANGE_COEFF*((ranges(1) - RANGE_OFF)^2))*[cos(-base_angle),sin(-base_angle)]';

% Left Sensor
f_range2 = -1/(RANGE_COEFF*((ranges(2) - RANGE_OFF)^2))*[cos(base_angle),sin(base_angle)]';

f_ranges = f_range1 + f_range2;