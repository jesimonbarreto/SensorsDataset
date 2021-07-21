import os
from scipy.io import loadmat
from Dataset.Datasets import Dataset
from enum import Enum
import numpy as np


class SignalsUschad(Enum):
    acc_front_right_hip_X = 0
    acc_front_right_hip_Y = 1
    acc_front_right_hip_Z = 2
    gyr_front_right_hip_X = 3
    gyr_front_right_hip_Y = 4
    gyr_front_right_hip_Z = 5


actNameUschad = {
    1:  'Walking Forward',
    2:  'Walking Left',
    3:  'Walking Right',
    4:  'Walking Up',
    5:  'Walking Down',
    6:  'Running',
    7:  'Jumping',
    8:  'Sitting',
    9:  'Standing',
    10: 'Sleeping',
    11: 'Elevator Up',
    12: 'Elevator Down',
}


class USCHAD(Dataset):
    def __init__(self, name, dir_dataset, dir_save, freq = 100, trials_per_file=100000):
        super().__init__(name, dir_dataset, dir_save, freq = freq, trials_per_file=trials_per_file)
        self.activitiesDict = actNameUschad
        self.wind = None
    def print_info(self):
        return """
                device: IMU
                frequency: 100Hz
                positions: front-right-hip
                sensors: acc and gyr
                """

    def fix_name_act(self, act):
        if "running" in act:
            act = act.replace("running", "run")
        if "jumping" in act:
            act = act.replace("jumping", "jump")
        if "sitting" in act:
            act = act.replace("sitting", "sit")
        if "standing" in act:
            act = act.replace("standing", "stand")
        if "downstairs" in act:
            act = act.replace("downstairs", "down")
        if "walking" in act:
            act = act.replace("walking", "walk")
        if "upstairs" in act:
            act = act.replace("upstairs", "up")
        return act

    def preprocess(self):
        mat_files = []
        for root, dirs, files in os.walk(self.dir_dataset):
            if len(dirs) == 0:
                mat_files.extend([os.path.join(root, f) for f in files])

        for filepath in mat_files:
            mat_file = loadmat(filepath)
            act = mat_file['activity'][0]
            subject = int(mat_file['subject'][0])
            trial_id = int(mat_file['trial'][0])
            trial_data = mat_file['sensor_readings'].astype('float64')

            data = []
            for d in self.signals_use:
                data.append(trial_data[:, d.value])
            trial = np.column_stack(data).astype('float64')
            act = act.replace("-", " ")
            act = self.fix_name_act(act)
            self.add_info_data(act, subject, trial_id, trial, self.dir_save)

        self.save_data(self.dir_save)