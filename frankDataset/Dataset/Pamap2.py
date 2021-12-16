from Dataset import Dataset
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
    1:  'Lying',
    2:  'Sitting',
    3:  'Standing',
    4:  'Walking',
    5:  'Running',
    6:  'cycling',
    7:  'Nordic walking',
    9:  'watching TV',
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
    0:  'other (transient activities)'
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
         
    def rename_act(self, act):
        act = act.lower()
        if act == 'ascending stairs':
            return 'upstairs'
        if act == 'descending stairs':
            return 'downstairs'
        else:
            return act

    def preprocess(self):
        files = glob.glob(pathname=os.path.join(self.dir_dataset, "Optional", '*.dat'))
        files.extend(glob.glob(pathname=os.path.join(self.dir_dataset, "Protocol",'*.dat')))
        output_dir = self.dir_save

        for f in files:
            fmt_data = {}
            subject = int(f[-7:-4])
            
            with open(f, 'r') as inp:
                instances = [list(map(float, line.split())) for line in inp.read().splitlines()]
            
            cur_act = instances[0][1]
            trial = []
            for instance in instances:
                act_id = int(instance[1])
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

                        # Sort by timestamp
                        trial = trial[trial[:, 0].argsort()]

                        signals = [signal.value for signal in self.signals_use]
                        trial = trial[:, signals]

                        # Filtro de NaNs
                        # indexes = np.sum(~np.isnan(trial), axis=1) == 54
                        # trial = trial[indexes]

                        act = actNamePAMAP2[act_id]
                        act = self.rename_act(act)
                        self.add_info_data(act, subject, trial_id, trial, output_dir)
        self.save_data(output_dir)