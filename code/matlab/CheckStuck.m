function [stuck_timer, rand_goal] = CheckStuck(poses, VAR_THRESH, stuck_timer, rand_goal)

pose_var = [var(poses(1,:)), var(poses(2,:))]';
if((pose_var(1) < VAR_THRESH) && ~any(poses(1,:) == 0) && (stuck_timer.stuck == 0))
    rand_goal = 500*rand(2,1);
    stuck_timer.time = stuck_timer.top;
    stuck_timer.count = stuck_timer.count + 1;
    stuck_timer = stuck_timer.updateTop();
    stuck_timer.stuck = 1;
    disp('BANG X');
elseif ((pose_var(2) < VAR_THRESH) && ~any(poses(2,:) == 0) && (stuck_timer.stuck == 0))
    rand_goal = 500*rand(2,1);
    stuck_timer.time = stuck_timer.top;
    stuck_timer.count = stuck_timer.count + 1;
    stuck_timer = stuck_timer.updateTop();
    stuck_timer.stuck = 1;
    disp('BANG Y');
end
