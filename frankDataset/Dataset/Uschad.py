import os
from scipy.io import loadmat
from Dataset.Datasets import Dataset
from enum import Enum
import numpy as np


class SignalsUSCHAD(Enum):
    acc_front_right_hip_X = 0
    acc_front_right_hip_Y = 1
    acc_front_right_hip_Z = 2
    gyr_front_right_hip_X = 3
    gyr_front_right_hip_Y = 4
    gyr_front_right_hip_Z = 5


actNameUSCHAD = {
    1:  'Walk Forward',
    2:  'Walk Left',
    3:  'Walk Right',
    4:  'Walk Up',
    5:  'Walk Down',
    6:  'Run',
    7:  'Jump',
    8:  'Sit',
    9:  'Stand',
    10: 'Sleeping',
    11: 'Elevator Up',
    12: 'Elevator Down',
}


def rename_act(act):
    act = act.lower()
    if act == 'walk forward':
        return 'walking'
    if act == 'walk up':
        return 'upstairs'
    if act == 'walk downstairs':
        return 'downstairs'
    if act == 'sit':
        return 'sitting'
    if act == 'stand':
        return 'standing'
    if act == 'sleeping':
        return 'lying'
    if act == 'run':
        return 'running'
    else:
        return act


def fix_name_act(act):
    """
    There is annotations of the same
    class if different label
    This code corrects it
    """

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


class USCHAD(Dataset):
    def print_info(self):
        return """
                device: IMU
                frequency: 100Hz
                positions: front-right-hip
                sensors: acc and gyr
                """

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
            act = fix_name_act(act)
            act = rename_act(act)
            self.add_info_data(act, subject, trial_id, trial, self.dir_save)

        self.save_data(self.dir_save)
