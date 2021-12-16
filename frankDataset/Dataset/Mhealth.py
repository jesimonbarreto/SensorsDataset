from .Datasets import Dataset
import glob, os
import numpy as np
from enum import Enum


class SignalsMHEALTH(Enum):
    acc_chest_X = 0
    acc_chest_Y = 1 
    acc_chest_Z = 2
    elecd_l1 = 3
    elecd_l2 = 4 
    acc_left_ankle_X = 5
    acc_left_ankle_Y = 6
    acc_left_ankle_Z = 7
    gyr_left_ankle_X = 8
    gyr_left_ankle_Y = 9 
    gyr_left_ankle_Z = 10
    mag_left_ankle_X = 11
    mag_left_ankle_Y = 12
    mag_left_ankle_Z = 13
    acc_right_lower_arm_X = 14
    acc_right_lower_arm_Y = 15
    acc_right_lower_arm_Z = 16
    gyr_right_lower_arm_X = 17
    gyr_right_lower_arm_Y = 18
    gyr_right_lower_arm_Z = 19
    mag_right_lower_arm_X = 20
    mag_right_lower_arm_Y = 21
    mag_right_lower_arm_Z = 22


actNameMHEALTH = {
    0:  'Nothing',
    1:  'Standing',
    2:  'Sitting',
    3:  'Lying down',
    4:  'Walking',
    5:  'Climbing stairs',
    6:  'Waist bends forward',
    7:  'Frontal elevation of lower arms',
    8:  'Knees bending (crouching)',
    9:  'Cycling',
    10: 'Jogging',
    11: 'Running',
    12: 'Jump front & back'
}


class MHEALTH(Dataset):
    def print_info(self):
        return """
                device: IMU
                frequency: 50Hz
                positions: chest, left ankle and right lower arm
                sensors:acc, gyr, mag, eletrocardiogram
                """

    def rename_act(self, act):
        act = act.lower()
        if act == 'climbing stairs':
            return 'upstairs'
        if act == 'lying down':
            return 'lying'
        else:
            return act

    def preprocess(self):
        files = glob.glob(os.path.join(self.dir_dataset,'*.log')) #glob.glob(pathname='*.log')
        output_dir = self.dir_save  #'../output'
        for f in files:
            if '.log' not in f:
                continue

            fmt_data = {}
            start = -6 if f[-6].isnumeric() else -5
            subject = int(f[start:-4])
            
            with open(f, 'r') as inp:
                instances = [list(map(float, line.split())) for line in inp.read().splitlines()]
            
            cur_act = instances[0][-1]
            trial = []
            for instance in instances:
                act_id = int(instance[-1])      
                if act_id not in fmt_data:
                    fmt_data[act_id] = {}

                if cur_act != act_id:
                    trial_id = max(list(fmt_data[act_id].keys())) if len(list(fmt_data[act_id].keys())) > 0 else 0
                    fmt_data[act_id][trial_id + 1] = trial
                    cur_act = act_id
                    trial = []

                trial.append(instance)

            for act_id in fmt_data.keys():
                if act_id != 0:
                    for trial_id, trial in fmt_data[act_id].items():
                        trial = np.array(trial)

                        signals = [signal.value for signal in self.signals_use]
                        trial = trial[:, signals]

                        # Filtro de NaNs
                        # indexes = np.sum(~np.isnan(trial), axis=1) == 54
                        # trial = trial[indexes]

                        act = actNameMHEALTH[act_id]
                        act = self.rename_act(act)
                        self.add_info_data(act, subject, trial_id, trial, output_dir)
        self.save_data(output_dir)