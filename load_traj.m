% function [data, info] = load_traj(file, vsize)
function [data, info] = load_traj(file, vsize)

fid=fopen(file);

data = fread(fid, [vsize, inf], 'float32');
info=size(data);

fclose(fid);