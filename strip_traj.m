% 3.2.7 strip the original trajectories
clear; close all;

f0 = load_traj('utt1.f0', 1);
mcep = load_traj('utt1.mcep', 60);
apf = load_traj('utt1.apf', 21);

save_traj('traj-strip/utt1.mcep', mcep(:, 1:548));
save_traj('traj-strip/utt1.f0', f0(:, 1:548));
save_traj('traj-strip/utt1.apf', apf(:, 1:548));
save_traj_double('traj-strip/utt1.apf.double', apf(:, 1:548));

fid = fopen('traj-strip/utt1.f0.txt','w');
fprintf(fid, '%d\n', f0(:, 1:548));
fclose(fid);