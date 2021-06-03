from .Datasets import Dataset
import numpy as np
import glob, os
from enum import Enum

class SignalsPAMAP2(Enum):
    timestamp = 0
    activityID = 1
    heart_rate_bpm = 2
    temp_dominant_wrist = 3
    acc1_dominant_wrist_X = 4
    acc1_dominant_wrist_Y = 5 
    acc1_dominant_wrist_Z = 6
    acc2_dominant_wrist_X = 7
    acc2_dominant_wrist_Y = 8 
    acc2_dominant_wrist_Z = 9
    gyr_dominant_wrist_X = 10
    gyr_dominant_wrist_Y = 11
    gyr_dominant_wrist_Z = 12
    mag_dominant_wrist_X = 13
    mag_dominant_wrist_Y = 14
    mag_dominant_wrist_Z = 15
    orientation_dominant_wrist_1 = 16
    orientation_dominant_wrist_2 = 17
    orientation_dominant_wrist_3 = 18
    orientation_dominant_wrist_4 = 19
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
    orientation_chest_1 = 33
    orientation_chest_2 = 34
    orientation_chest_3 = 35
    orientation_chest_4 = 36
    temp_dominant_ankle = 37
    acc1_dominant_ankle_X = 38
    acc1_dominant_ankle_Y = 39 
    acc1_dominant_ankle_Z = 40
    acc2_dominant_ankle_X = 41
    acc2_dominant_ankle_Y = 42 
    acc2_dominant_ankle_Z = 43
    gyr_dominant_ankle_X = 44
    gyr_dominant_ankle_Y = 45
    gyr_dominant_ankle_Z = 46
    mag_dominant_ankle_X = 47
    mag_dominant_ankle_Y = 48
    mag_dominant_ankle_Z = 49
    orientation_dominant_ankle_1 = 50
    orientation_dominant_ankle_2 = 51
    orientation_dominant_ankle_3 = 52
    orientation_dominant_ankle_4 = 53


actNamePAMAP2 = {
    1: 'Lying',
    2: 'Sitting',
    3: 'Standing',
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
    def print_info(self):
        return """
                device: IMU
                frequency: 100Hz
                positions: dominant wrist, chest and dominant side's ankle
                sensors: heart rate, temperature, acc, gyr and mag
                """

    def clean_data_not_used(self, sample):
        sample[SignalsPAMAP2.heart_rate_bpm] = '0'
        sample[SignalsPAMAP2.orientation_chest_1] = '0'
        sample[SignalsPAMAP2.orientation_chest_2] = '0'
        sample[SignalsPAMAP2.orientation_chest_3] = '0'
        sample[SignalsPAMAP2.orientation_chest_4] = '0'
        sample[SignalsPAMAP2.orientation_dominant_ankle_1] = '0'
        sample[SignalsPAMAP2.orientation_dominant_ankle_2] = '0'
        sample[SignalsPAMAP2.orientation_dominant_ankle_3] = '0'
        sample[SignalsPAMAP2.orientation_dominant_ankle_4] = '0'
        sample[SignalsPAMAP2.orientation_dominant_wrist_1] = '0'
        sample[SignalsPAMAP2.orientation_dominant_wrist_2] = '0'
        sample[SignalsPAMAP2.orientation_dominant_wrist_3] = '0'
        sample[SignalsPAMAP2.orientation_dominant_wrist_4] = '0'
        return sample
         

    def preprocess(self):
        files = glob.glob(pathname=os.path.join(self.dir_dataset, "Optional", '*.dat'))
        files.extend(glob.glob(pathname=os.path.join(self.dir_dataset, "Protocol",'*.dat')))
        output_dir = self.dir_save #'../output/2'
        subject = 0
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            for line in lines:
                split = line.strip().split(' ')
                act = split[1]
                if act != '0':
                    sample = []
                    for d in self.signals_use:
                        smp = float(split[d.value])
                        sample.append(smp)

                    trial.append(sample)
                    # It is not the same trial
                    if iterator == len(lines)-1 or lines[iterator+1].split(' ')[1] != act:

                        act_name = actNamePAMAP2[int(act)]
                        self.add_info_data(act_name, subject, trial_id, trial, output_dir)
                        trial_id = trial_id + 1
                        trial = []

                iterator = iterator + 1
            #print('file_name:[{}] s:[{}]'.format(file, subject))
            #print('{} incorrect lines in file {}'.format(str(incorrect), file))
        self.save_data(output_dir)