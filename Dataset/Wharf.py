import os

import numpy as np

from Dataset.Datasets import Dataset


actNameWHARF = {
    1:  'Brush teeth',
    2:  'Climb stairs',
    3:  'Comb hair',
    4:  'Descend stairs',
    5:  'Drinking glass',
    6:  'Eat meat',
    7:  'Ead soup',
    8:  'Get up bed',
    9:  'Lie down bed',
    10: 'Pour water',
    11: 'Sit down chair',
    12: 'Stand up chair',
    13: 'Walk',
    14: 'Use telephone'
}


class WHARF(Dataset):
    def preprocess(self):
        txt_files = []
        for root, dirs, files in os.walk(self.dir_dataset):
            if len(dirs) == 0:
                txt_files.extend([os.path.join(root, f) for f in files if '.txt' in f])

        print(len(txt_files))

        for trial_id, filepath in enumerate(txt_files):
            with open(filepath, 'r') as f:
                filename = filepath.split(os.sep)[-1]
                act, subject = filename.split('-')[-2:]
                subject = subject.replace('.txt', '')
                trial = f.read().split()
                trial = list(map(int, trial))
                trial = np.array(trial).reshape(-1, 3)

                self.add_info_data(act, subject, trial_id, trial, self.dir_save)
                print('file_name:[{}] s:[{}]'.format(filepath, subject))

        self.save_data(self.dir_save)



