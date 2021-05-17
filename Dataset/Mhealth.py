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
    acc_left_ankle_X = 4
    acc_left_ankle_Y = 5
    acc_left_ankle_Z = 6
    gyr_left_ankle_X = 7
    gyr_left_ankle_Y = 8 
    gyr_left_ankle_Z = 9
    mag_left_ankle_X = 10
    mag_left_ankle_Y = 11
    mag_left_ankle_Z = 12
    acc_right_arm_X = 13
    acc_right_arm_Y = 14
    acc_right_arm_Z = 15
    gyr_right_arm_X = 16
    gyr_right_arm_Y = 17
    gyr_right_arm_Z = 18
    mag_right_arm_X = 19
    mag_right_arm_Y = 20
    mag_right_arm_Z = 21

actNameMHEALTH = {0:'nothing',1:'Standing',2: 'Sitting', 3: 'Lying down', 4:'Walking', 5: 'Climbing stairs', 
                    6: 'Waist bends forward', 7: 'Frontal elevation of arms', 8: 'Knees bending (crouching)',
                    9: 'Cycling', 10: 'Jogging', 11: 'Running', 12: 'Jump front & back'}
class MHEALTH(Dataset):

    def action_code_to_name(self, act):
        new_act = []
        for a in act:
            new_act.append(actNameMHEALTH[int(a)])
        return new_act

    def preprocess(self):
        files = glob.glob(os.path.join(self.dir_dataset,'*.log')) #glob.glob(pathname='*.log')
        output_dir = self.dir_save  #'../output'

        subject = 0
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            for line in lines:
                split = line.strip().split('\t')
                columns = len(split)-1
                if len(split) < 24:
                    print('Error')
                
                act = split[columns]


                #It is the same trial
                if iterator != len(lines)-1 and lines[iterator+1].split('\t')[len(split)-1].replace('\n','') == act:
                    if len(self.signals_use)>0:
                        data = []
                        for d in self.signals_use:
                            data.append(split[d.value])
                        dc = np.column_stack(data)
                    else:
                        dc = split[0:columns]
                    trial.append(dc)
                
                #The next line will be a novel trial
                else:
                    #act = self.action_code_to_name(act)
                    act = actNameMHEALTH[int(act)]
                    self.add_info_data(act, subject, trial_id, trial, output_dir)
                    trial_id = trial_id + 1
                    trial = []

                iterator = iterator + 1
            
            #print('file_name:[{}] s:[{}]'.format(file, subject))
        self.save_data(output_dir)