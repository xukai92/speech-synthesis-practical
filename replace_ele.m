% 3.2.7 generate the trajctories using the original parameters
clear; close all;

htkdata = load_htkdata('utt1_original.cmp');

mcep = htkdata(1:60, :);
f0 = htkdata(181, :);
f0(f0 == -1.0000e+10) = 0;
apf = htkdata(184:204, :);

save_traj('traj-replaced/utt1.mcep', mcep);
save_traj('traj-replaced/utt1.f0', f0);
save_traj('traj-replaced/utt1.apf', apf);
save_traj_double('traj-replaced/utt1.apf.double', apf);

fid = fopen('traj-replaced/utt1.f0.txt','w');
fprintf(fid, '%d\n', f0);
fclose(fid);