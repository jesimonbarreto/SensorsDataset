from .Datasets import Dataset
import numpy as np
import pandas as pd
import glob, os
from enum import Enum

class SignalsUCIHAR(Enum):
	acc_body_X = 0
	acc_body_Y = 1
	acc_body_Z = 2
	gyr_body_X = 3
	gyr_body_Y = 4
	gyr_body_Z = 5
	acc_total_X = 6
	acc_total_Y = 7
	acc_total_Z = 8
	


actNameUCIHAR = {
	1: 'Walking',
	2: 'Ascending stairs',
	3: 'Descending stairs',
	4: 'Sitting',
	5: 'Standing',
	6: 'Laying'
}

class UCIHAR(Dataset):
	def print_info(self):
		return "device:  smartphone (Samsung Galaxy S II)" \
		       "frequency: 50 Hz" \
		       "positions: waist" \
		       "sensors: accelerometer, gyroscope" \
		       "subjects: 50" \
		       "Age: 19-48"
		
	def preprocess(self):
		dataFiles = os.path.join(self.dir_dataset,'original','UCI HAR Dataset')
		trial_id =np.zeros([30])
		for part in ['train','test']:
			data = []
			path = os.path.join(dataFiles, part, 'Inertial Signals')
			for sig in ['body_acc','body_gyro','total_acc']:
				for axis in ['x','y','z']:
					data.append(pd.read_csv(os.path.join(path,f'{sig}_{axis}_{part}.txt'),delim_whitespace=True, header=None))
		
	
			subjects = pd.read_csv(os.path.join(self.dir_dataset,'original',f'subject_{part}.csv'))
			labels = pd.read_csv(os.path.join(self.dir_dataset,'original',f'y_{part}.csv'))
			for i in range(len(labels)):
				trial =None
				for d in data:
					if trial is not None:
						trial = np.concatenate([trial,np.expand_dims(d.iloc[i,:].values,1)],axis = 1)
					else:
						trial = np.expand_dims(d.iloc[i,:].values,1)
				act = actNameUCIHAR[labels.iloc[i].values[0]]
				signals = [signal.value for signal in self.signals_use]
				trial = trial[:, signals]
				subj = subjects.iloc[i].values[0] -1
				self.add_info_data(act, subj, trial_id[subj], trial, self.dir_save)
				trial_id[subj] +=1
		self.save_data(self.dir_save)

			

		
			


