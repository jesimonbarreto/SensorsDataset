from Dataset.Datasets import Dataset
import numpy as np
import glob
import os
from scipy.io import loadmat

actNameUTDMHAD2 = {
        22: 'jogging',
        23: 'walking',
        24: 'sit to stand',
        25: 'stand to sit',
        26: 'forward lunge',
        27: 'squat'}


class UTDMHAD2(Dataset):
    def preprocess(self):
        activities = np.arange(22, 28)
        pathname = os.path.join(self.dir_dataset, '*.mat')
        files = glob.glob(pathname=pathname)

        for f in files:
            act = int(os.path.split(f)[-1].split("_")[0].split("a")[-1])
            subject = int(os.path.split(f)[-1].split("_")[1].split("s")[-1])
            trial_id = int(os.path.split(f)[-1].split("_")[2].split("t")[-1])
            trial = loadmat(f)['d_iner'][:, 0:3]
            if act in activities:
                act_name = actNameUTDMHAD2[act]
                #print('{} {} {}'.format(act_name, subject, trial_id))
                self.add_info_data(act_name, subject, trial_id, trial, self.dir_save)

        self.save_data(self.dir_save)