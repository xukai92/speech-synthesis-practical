% 3.2.6
clear; close all;

htkdata = load_htkdata('utt1_original.cmp');

f0 = load_traj('utt1.f0', 1);
% f0_aligned = load_traj('traj-dur/utt1.f0', 1);
% f0_original = htkdata(181, :);
% f0_original(f0_original == -1.0000e+10) = 0;

mcep = load_traj('utt1.mcep', 60);
mcep = mcep(4, :);
% mcep_aligned = load_traj('traj-dur/utt1.mcep', 60);
% mcep_aligned = mcep_aligned(4, :);
% mcep_original = htkdata(4, :);

apf = load_traj('utt1.apf', 21);
apf = apf(1, :);
% apf_aligned = load_traj('traj-dur/utt1.apf', 21);
% apf_aligned = apf_aligned(1, :);
% apf_original = htkdata(184, :);

figure('position', [0, 0, 800, 400])
plot(f0); hold on;
% plot(f0_aligned); hold on; 
% plot(f0_original); hold on;
title('Plot of the fudemental frequency (f0)');
xlabel('frame'); ylabel('value');
% legend('syn', 'syn aligned','original');

figure('position', [0, 0, 800, 400])
plot(mcep); hold on;
% plot(mcep_aligned); hold on; 
% plot(mcep_original); hold on;
title('Plot of the 4th dimension of the mel-cepstrum (mcep)');
xlabel('frame'); ylabel('value');
% legend('syn', 'syn aligned','original'); 

figure('position', [0, 0, 800, 400])
plot(apf); hold on;
% plot(apf_aligned); hold on; 
% plot(apf_original); hold on;
title('Plot of the 1st dimension of the aperiodicity (apf)');
xlabel('frame'); ylabel('value');
% legend('syn', 'syn aligned','original'); 