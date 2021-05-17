from .Datasets import Dataset
import numpy as np
import glob, os
from enum import Enum

class SignalsPAMAP2(Enum):
    timestamp = 0
    activityID = 1
    heart_rate_bpm = 2
    temp_hand = 3
    acc1_hand_X = 4
    acc1_hand_Y = 5 
    acc1_hand_Z = 6
    acc2_hand_X = 7
    acc2_hand_Y = 8 
    acc2_hand_Z = 9
    gyr_hand_X = 10
    gyr_hand_Y = 11
    gyr_hand_Z = 12
    mag_hand_X = 13
    mag_hand_Y = 14
    mag_hand_Z = 15
    orientation_hand_1=16
    orientation_hand_2=17
    orientation_hand_3=18
    orientation_hand_4=19
    temp_chest = 20
    acc1_chest_X = 21
    acc1_chest_Y = 22 
    acc1_chest_Z = 23
    acc2_chest_X = 24
    acc2_chest_Y = 25 
    acc2_chest_Z = 26
    gyr_chest_X = 27
    gyr_chest_Y = 28
    gyr_chest_Z = 29
    mag_chest_X = 30
    mag_chest_Y = 31
    mag_chest_Z = 32
    orientation_chest_1=33
    orientation_chest_2=34
    orientation_chest_3=35
    orientation_chest_4=36
    temp_ankle = 37
    acc1_ankle_X = 38
    acc1_ankle_Y = 39 
    acc1_ankle_Z = 40
    acc2_ankle_X = 41
    acc2_ankle_Y = 42 
    acc2_ankle_Z = 43
    gyr_ankle_X = 44
    gyr_ankle_Y = 45
    gyr_ankle_Z = 46
    mag_ankle_X = 47
    mag_ankle_Y = 48
    mag_ankle_Z = 49
    orientation_ankle_1=50
    orientation_ankle_2=51
    orientation_ankle_3=52
    orientation_ankle_4=53

actNamePAMAP2 = {
    1:'Lying',
    2:'Sitting',
    3:'Standing',
    4: 'Walking',
    5: 'Running',
    6: 'cycling',
    7: 'Nordic walking',
    9: 'watching TV',
    10: 'computer work',
    11: 'car driving',
    12: 'ascending stairs',
    13: 'descending stairs',
    16: 'vacuum cleaning',
    17: 'ironing',
    18: 'folding laundry',
    19: 'house cleaning',
    20: 'playing soccer',
    24: 'rope jumping',
    0: 'other (transient activities)'
}
class PAMAP2(Dataset):
    def action_code_to_name(self, act):
        new_act = []
        for a in act:
            new_act.append(actNamePAMAP2[int(a)])
        return new_act

    def preprocess(self):
        files = glob.glob(pathname=os.path.join(self.dir_dataset,'*.dat'))#'Optional/*.dat')
        output_dir = self.dir_save #'../output/2'
        idx_label = 1
        subject = 0
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            incorrect = 0
            for line in lines:
                split = line.strip().split(' ')
                sample =  np.asarray(split)
                act = sample[1]
                if act != '0':
                    data = []
                    for d in self.signals_use:
                        data.append(sample[d.value])
                    sample = np.column_stack(data)
                    #sample = np.delete(sample, remove_columns)

                    #It is the same trial
                    #lines[iterator + 1].split(' ')[1] is the next activity
                    if iterator != len(lines)-1 and lines[iterator+1].split(' ')[1] == act:
                        idx = np.where(sample == 'NaN')[0]
                        if(idx.size==0):
                            trial.append(sample)
                        else:#Incorrect file
                            incorrect = incorrect+1

                    #The next line will be a novel trial
                    else:
                        #act = self.action_code_to_name(act)
                        act = actNamePAMAP2[int(act)]
                        self.add_info_data(act, subject, trial_id, trial, output_dir)
                        #self.save_file(act, subject, trial_id, trial)
                        trial_id = trial_id + 1
                        trial = []


                    iterator = iterator + 1
            #print('file_name:[{}] s:[{}]'.format(file, subject))
            #print('{} incorrect lines in file {}'.format(str(incorrect), file))
        self.save_data(output_dir)