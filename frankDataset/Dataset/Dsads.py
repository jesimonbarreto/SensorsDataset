from .Datasets import Dataset
import numpy as np
import pandas as pd
import glob, os
from enum import Enum
import scipy.io


class SignalsDsads(Enum):
	acc_torso_X = 0
	acc_torso_Y = 1
	acc_torso_Z = 2
	gyr_torso_X = 3
	gyr_torso_Y = 4
	gyr_torso_Z = 5
	mag_torso_X = 6
	mag_torso_Y = 7
	mag_torso_Z = 8
	acc_right_arm_X = 9
	acc_right_arm_Y = 10
	acc_right_arm_Z = 11
	gyr_right_arm_X = 12
	gyr_right_arm_Y = 13
	gyr_right_arm_Z = 14
	mag_right_arm_X = 15
	mag_right_arm_Y = 16
	mag_right_arm_Z = 17
	acc_left_arm_X = 18
	acc_left_arm_Y = 19
	acc_left_arm_Z = 20
	gyr_left_arm_X = 21
	gyr_left_arm_Y = 22
	gyr_left_arm_Z = 23
	mag_left_arm_X = 24
	mag_left_arm_Y = 25
	mag_left_arm_Z = 26
	acc_right_leg_X = 27
	acc_right_leg_Y = 28
	acc_right_leg_Z = 29
	gyr_right_leg_X = 30
	gyr_right_leg_Y = 31
	gyr_right_leg_Z = 32
	mag_right_leg_X = 33
	mag_right_leg_Y = 34
	mag_right_leg_Z = 35
	acc_left_leg_X = 36
	acc_left_leg_Y = 37
	acc_left_leg_Z = 38
	gyr_left_leg_X = 39
	gyr_left_leg_Y = 40
	gyr_left_leg_Z = 41
	mag_left_leg_X = 42
	mag_left_leg_Y = 43
	mag_left_leg_Z = 44

	

actNameDsads = {
	1:  'Sitting',
	2:  'Standing',
	3:  'Lying on back',
	4:  'lying on right',
	5:  'Ascending stairs',
	6:  'Descending stairs',
	7:  'Standing in an elevator',
	8:  'Moving around in an elevator',
	9:  'Walking', # walking in a parking lot
	10: 'Walking on a treadmill (4 km/h - flat)',
	11: 'Walking on a treadmill (4 km/h - 15 deg inclined)',
	12: 'Running on a treadmill (8 km/h)',
	13: 'Exercising on a stepper',
	14: 'Exercising on a cross trainer',
	15: 'Cycling (horizontal)', #cycling on an exercise bike in horizontal
	16: 'Cycling (vertical)',
	17: 'Rowing',
	18: 'Jumping',
	19: 'Playing basketball '
}


class DSADS(Dataset):
	def __init__(self, name, dir_dataset, dir_save, freq = 25, trials_per_file=10000):
		super().__init__(name, dir_dataset, dir_save, freq = freq, trials_per_file=trials_per_file)
		self.activitiesDict = actNameDsads
		self.wind = 5
	
	def print_info(self):
		return "device:  smartphone (Samsung Galaxy S II)" \
		       "frequency: 25 Hz" \
		       "positions: torso,rightArm,leftArm,RightLeg,leftLeg" \
		       "sensors: accelerometer, gyroscope,magnetometer" \
		       "subjects: 8 (4 female, 4 male)" \
		       "Age:  20-30" \
		       "5 seg per sample"
	
	def preprocess(self):
		dataFiles = os.path.join(self.dir_dataset, 'original')
		aux = os.listdir(dataFiles)
		if len(aux) == 1 and aux[0].split('.')[-1] == '.zip':
			#unzip the file
			pass
		dataFiles = os.path.join(dataFiles,'data')
		for act in os.listdir(dataFiles):
			fileSub = os.path.join(dataFiles,act)
			for subj in os.listdir(fileSub):
				trialFile = os.path.join(fileSub,subj)
				for trial_id,trial in enumerate(glob.glob(os.path.join(trialFile,'*.txt'))):
					data = os.path.join(trialFile,trial)
					trialData = np.loadtxt(data, delimiter=',')
					data = []
					for d in self.signals_use:
						data.append(trialData[:, d.value])
					data = np.transpose(np.array(data).astype('float64') , (1, 0))
					act_name = actNameDsads[np.int(act[-2:])]
					self.add_info_data(act_name, np.int(subj[1:]), trial_id, data, self.dir_save)
		self.save_data(self.dir_save)
