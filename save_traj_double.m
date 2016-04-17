% function [data, info] = save_traj(file, data)
function save_traj_double(file, data)

fid=fopen(file, 'w');

fwrite(fid, data, 'double');

fclose(fid);