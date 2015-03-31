classdef StuckTimer
    %UNTITLED7 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        stuck = 0;
        time = 0;
        count = 0;
        top = 100;
    end
    
    methods
        function obj = updateTop(obj)
            obj.top = obj.count*100;
        end
    end
    
end

