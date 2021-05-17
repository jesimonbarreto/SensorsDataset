from .Datasets import Dataset
import numpy as np
import glob
import os
from scipy.io import loadmat
from enum import Enum


class SignalsUtdmhad2(Enum):
    acc_right_thigh_X = 1
    acc_right_thigh_Y = 2 
    acc_right_thigh_Z = 3
    gyr_right_thigh_X = 4
    gyr_right_thigh_Y = 5
    gyr_right_thigh_Z = 6


actNameUTDMHAD2 = {
        22: 'Jogging',
        23: 'Walking',
        24: 'Sit to stand',
        25: 'Stand to sit',
        26: 'Forward lunge',
        27: 'Squat'}


class UTDMHAD2(Dataset):
    def print_info(self):
        return """
                device: IMU
                frequency: 50hz
                positions: right thigh
                sensors: acc and gyr
                """

    def preprocess(self):
        activities = np.arange(22, 28)
        pathname = os.path.join(self.dir_dataset, '*.mat')
        files = glob.glob(pathname=pathname)

        for f in files:
            act = int(os.path.split(f)[-1].split("_")[0].split("a")[-1])
            subject = int(os.path.split(f)[-1].split("_")[1].split("s")[-1])
            trial_id = int(os.path.split(f)[-1].split("_")[2].split("t")[-1])
            samples = loadmat(f)['d_iner']
            data = []
            for d in self.signals_use:
                data.append(samples[:,d.value]) #[:, 0:3]
            trial = np.column_stack(data)
            if act in activities:
                act_name = actNameUTDMHAD2[act]
                #print('{} {} {}'.format(act_name, subject, trial_id))
                self.add_info_data(act_name, subject, trial_id, trial, self.dir_save)

        self.save_data(self.dir_save)