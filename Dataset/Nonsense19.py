from .Datasets import Dataset
import numpy as np
import glob
import os
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

class NonSense(Dataset):
	#http://www.mica.edu.vn/perso/Le-Thi-Lan/19NonSense.html
	def preprocess(self):
		first = True
		#data_dir = '19NonSense/'
		files = glob.glob(self.dir_dataset + '/0*')
		#folds = []
		X = np.array([])
		y = np.array([])
		#iterating through the subjects:
		for sub_dir in files[:-1]:
			path = os.path.join(self.dir_dataset, sub_dir)
			x_aux = np.load(os.path.join(path, 'in', 'X.npy'))
			y_aux = np.load(os.path.join(path, 'in', 'Y.npy'))
			x_aux = np.concatenate([x_aux, np.load(os.path.join(path, 'out', 'X.npy'))])
			y_aux = np.concatenate([y_aux, np.load(os.path.join(path, 'out', 'Y.npy'))])
			trial_id = 0
			for trial_x, trial_y in zip(x_aux, y_aux):
				self.add_info_data(act=trial_y,subject= sub_dir, trial_id = trial_id,trial= trial_x,output_dir= self.dir_save)
				trial_id +=1
			print(sub_dir)
		self.save_data(self.dir_save)
