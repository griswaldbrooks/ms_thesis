function poses = updatePoses(poses, v, om, dt)

    r_pose = [0,0,0]';
    r_pose(3) = poses(3,1) + om*dt;
    r_pose(1) = poses(1,1) + v*cos(r_pose(3));
    r_pose(2) = poses(2,1) + v*sin(r_pose(3));
    
    poses = [r_pose, poses(:, 1:length(poses) - 1)];
    %x = [var(poses(1,:)), var(poses(2,:))]'