% function [data, info] = save_traj(file, data)
function save_traj(file, data)

fid=fopen(file, 'w');

fwrite(fid, data, 'float32');

fclose(fid);