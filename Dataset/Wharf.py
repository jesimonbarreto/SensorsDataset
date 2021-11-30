import os

import numpy as np

from .Datasets import Dataset

from enum import Enum


class SignalsWharf(Enum):
    acc_right_wrist_X = 0
    acc_right_wrist_Y = 1
    acc_right_wrist_Z = 2


actNameWHARF = {
    1:  'Brush teeth',
    2:  'Climb stairs',
    3:  'Comb hair',
    4:  'Descend stairs',
    5:  'Drink glass',
    6:  'Eat meat',
    7:  'Eat soup',
    8:  'Getup bed',
    9:  'Liedown bed',
    10: 'Pour water',
    11: 'Sitdown chair',
    12: 'Standup chair',
    13: 'Walk',
    14: 'Use telephone'
}


class WHARF(Dataset):
    def print_info(self):
        return """
                device: IMU
                frequency: 32Hz
                positions: right wrist 
                sensors: acc
                """

    def rename_act(self, act):
        act = act.lower()
        if act == 'walk':
            return 'walking'
        if act == 'climb stairs':
            return 'upstairs'
        if act == 'sitdown chair':
            return 'sitting'
        if act == 'standup chair':
            return 'standing'
        if act == 'descend stairs':
            return 'downstairs'
        else:
            return act

    def preprocess(self):
        txt_files = []
        for root, dirs, files in os.walk(self.dir_dataset):
            if len(dirs) == 0:
                txt_files.extend([os.path.join(root, f) for f in files if '.txt' in f])

        print(len(txt_files))

        for trial_id, filepath in enumerate(txt_files):
            filename = filepath.split(os.sep)[-1]
            act, subject = filename.split('-')[-2:]
            act = act.replace("_", " ")
            act = self.rename_act(act)
            subject = subject.replace('.txt', '')
            with open(filepath, 'r') as inp:
                instances = [list(map(float, line.split())) for line in inp.read().splitlines()]

            trial = []
            for instance in instances:
                trial.append(instance)

            trial = np.array(trial)
            data = []
            for d in self.signals_use:
                data.append(trial[:,d.value])
            trial = np.column_stack(data).astype('float64')
            self.add_info_data(act, subject, trial_id, trial, self.dir_save)
            #print('file_name:[{}] s:[{}]'.format(filepath, subject))

        self.save_data(self.dir_save)



