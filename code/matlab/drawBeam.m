function drawBeam(view_angle, max_range, range, T, color)

% Transformed Beam Edges

    BEAM_X = max_range*cos(0.5*view_angle);
    BEAM_Y = max_range*sin(0.5*view_angle);
    beam_ep = zeros(3,2);
    beam_ep(:,1) = [BEAM_X,  BEAM_Y, 1]';
    beam_ep(:,2) = [BEAM_X, -BEAM_Y, 1]';
    beam_epT = zeros(3,2);

    beam_epT(:,1) = T*beam_ep(:,1);
    beam_epT(:,2) = T*beam_ep(:,2);
     
    line([T(1,3),beam_epT(1,1)],[T(2,3),beam_epT(2,1)],'Color',color);
    line([T(1,3),beam_epT(1,2)],[T(2,3),beam_epT(2,2)],'Color',color);
    
    for dth = (-0.5*view_angle):0.05:(0.5*view_angle)
        rx1 = range*cos(dth);
        ry1 = range*sin(dth);
        rx2 = range*cos(dth + 0.025);
        ry2 = range*sin(dth + 0.025);
        
        p1 = T*[rx1;ry1;1];
        p2 = T*[rx2;ry2;1];
        
        line([p1(1),p2(1)],[p1(2),p2(2)],'Color',color);
    end