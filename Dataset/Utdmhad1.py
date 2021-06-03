from .Datasets import Dataset
import numpy as np
import glob
import os
from scipy.io import loadmat
from enum import Enum


class SignalsUtdmhad1(Enum):
    acc_right_wrist_X = 1
    acc_right_wrist_Y = 2
    acc_right_wrist_Z = 3
    gyr_right_wrist_X = 4
    gyr_right_wrist_Y = 5
    gyr_right_wrist_Z = 6


actNameUTDMHAD1 = {
        1:  'right arm swipe to the left',
        2:  'right arm swipe to the right',
        3:  'right hand wave',
        4:  'two hand front clap',
        5:  'right arm throw',
        6:  'cross arms in the chest',
        7:  'basketball shooting',
        8:  'draw x',
        9:  'draw circle clockwise',
        10: 'draw circle counter clockwise',
        11: 'draw triangle',
        12: 'bowling',
        13: 'front boxing',
        14: 'baseball swing from right',
        15: 'tennis forehand swing',
        16: 'arm curl',
        17: 'tennis serve',
        18: 'two hand push',
        19: 'knock on door',
        20: 'hand catch',
        21: 'pick up and throw'
}


class UTDMHAD1(Dataset):
    def print_info(self):
        return """
                device: IMU
                frequency: 50Hz
                positions: right wrist
                sensors: acc and gyr
                """

    def preprocess(self):
        activities = np.arange(1, 22)
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
                act_name = actNameUTDMHAD1[act]
                #print('{} {} {}'.format(act_name, subject, trial_id))
                self.add_info_data(act_name, subject, trial_id, trial, self.dir_save)

        self.save_data(self.dir_save)
