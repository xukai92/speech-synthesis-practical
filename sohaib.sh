#!/bin/bash
cd /home/msa53/MLSALT10/Practical/
####################################

### Question 3.2.2
echo "Question 3.2.2 - DONE"
#echo "Generate the labels for the reference sentence using the supplied text analysis tool (Festival)"
#./scripts/txt2lab.sh original/txt/utt1.txt lab

### Question 3.2.3
echo "Question 3.2.3 - DONE"
#echo "Generate the trajectory of the model parameters using the label file above"
#./scripts/lab2traj.sh -hmmdir models/hts -labdir lab -outdir traj -filename utt1

# Question - is the nature of the trajectory as expected?

### Question 3.2.4
echo "Question 3.2.4 - DONE"
#./scripts/traj2wav.sh -trajdir traj -outdir wav -filename utt1

# Question - does it sound as expected?
# Sounds much more robotic than the original utterance (as expected), need to look at the spectogram for
# this but I expect to see sharper adjustments in speech (between phones) as opposed to the flowing dynamic
# that natural speech has, which is demonstrated in the first utterance.

### Question 3.2.5
echo "Question 3.2.5 - DONE"

# Make a copy of the file
#cp traj/utt1.f0.txt traj/utt1.f0.txt.orig

# Remove the existing file in case it exists
#rm -rf traj/utt1.f0.txt

# Make new file of all zero's
#python jobs/ques325.py traj/utt1.f0.txt 551

# Produce the new wav file
#./scripts/traj2wav.sh -trajdir traj -outdir wav -filename utt1

# Quality of the audio file is really bad when all the trajectories are zero.


echo "Question 3.2.6 - DONE"

#./scripts/lab2traj.sh -labdur -hmmdir models/hts -labdir original/lab -outdir traj-dur -filename utt1

# So this is a bit confusing but basically we generated trajectories before in question 3.2.3 and
# now we have generated the trajectories for the original set in 'lab'. Given this, you now have
# two folders (traj and traj-dur) that contain trajectories. From this, you can then amend or
# chop off pieces of to get the alignments and lengths sort of right. This is similar to dynamic
# time warping, which is effectively dynamic programming for time sequences.

# Moreover, you are then able to use the label files to look at how the adjustments are placed and
# could use this to reorder or amend the trajectories. To do this, take the label files and strip
# the first two columns. From here, plot the vertical time stamps on each trajectory (in my matlab)
# code and then you will know exactly what should be shifted where.'End effects' are where
# some silence frames may not be generated, which therefore must be appended to the end of the series.

# Seemingly it should only require the movement of two timesteps to get the f0's overlapping but mine
# are taking a few more...not sure why exactly but Im sure theres not much in it

echo "Question 3.2.7 - DONE"
# This requires the merging together of trajectories. So what I have done
# in the matlab script is to do: generated(generated>0)=original(generated>0),
# which should hopefully make the generated better. I would expect to do this
# for a number of different sequences (mel cepstrum, f0 and aperiodic) to see
# what difference it makes - shouldnt be too hard

echo "Question 3.3.1"

# Run the function to get the experts
#./scripts/getexpert.sh -hmmdir models/htk -labdir original/lab -stream 1 -dimension 4 -outdir expts -filename utt1
./scripts/getexpert.sh -hmmdir models/htk -labdir original/lab -stream 1 -dimension 60 -outdir expts2 -filename utt1
