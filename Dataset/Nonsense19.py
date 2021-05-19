from .Datasets import Dataset
import numpy as np
import glob
import os
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from enum import Enum


class SignalsNonSense(Enum):
    acc_foot_X = 0
    acc_foot_Y = 1
    acc_foot_Z = 2
    acc_wrist_X = 3
    acc_wrist_Y = 4
    acc_wrist_Z = 5
    gyr_wrist_X = 6
    gyr_wrist_Y = 7
    gyr_wrist_Z = 8


actNameNonSense = {
    1:  'Brushing',
    2:  'Washing hand',
    3:  'Slicing',
	4:  'Peeling',
	5:  'Upstairs',
	6:  'Downstairs',
	7:  'Mixing',
	8:  'Wiping',
	9:  'Sweeping floor',
	10: 'Turning shoulder',
	11: 'Turning wrist',
	12: 'Turning knee',
	13: 'Turning haunch',
	14: 'Turning ankle',
	15: 'Walking',
	16: 'Kicking',
	17: 'Running',
	18: 'Cycling',
	19: 'Null'
}


class NonSense(Dataset):
    # http://www.mica.edu.vn/perso/Le-Thi-Lan/19NonSense.html

    def print_info(self):
        return """
                device: Samsung G2 (smartwatch) and WAX3 sensor inside a shoe
                frequency: 50 Hz
                positions: Wrist (left or right) and foot
                sensors: Acelerometer and Gyr on the wrist and acelerometer on the foot
                """

    def preprocess(self):
        first = True
        # data_dir = '19NonSense/'
        files = glob.glob(self.dir_dataset + '/0*')
        # folds = []
        X = np.array([])
        y = np.array([])
        # iterating through the subjects:
        for sub_dir in files[:-1]:
            path = os.path.join(self.dir_dataset, sub_dir)
            x_aux = np.load(os.path.join(path, 'in', 'X.npy'))
            y_aux = np.load(os.path.join(path, 'in', 'Y.npy'))
            x_aux = np.concatenate([x_aux, np.load(os.path.join(path, 'out', 'X.npy'))])
            y_aux = np.concatenate([y_aux, np.load(os.path.join(path, 'out', 'Y.npy'))])
            trial_id = 0
            for trial_x, trial_y in zip(x_aux, y_aux):
                self.add_info_data(act=trial_y, subject=sub_dir, trial_id=trial_id, trial=trial_x,
                                   output_dir=self.dir_save)
                trial_id += 1
            print(sub_dir)
        self.save_data(self.dir_save)
