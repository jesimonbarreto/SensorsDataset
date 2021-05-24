import os

from scipy.io import loadmat

from Dataset.Datasets import Dataset

from enum import Enum


class SignalsUSCHAD(Enum):
    acc_front_right_hip_X = 1
    acc_front_right_hip_Y = 2 
    acc_front_right_hip_Z = 3
    gyr_front_right_hip_X = 4
    gyr_front_right_hip_Y = 5
    gyr_front_right_hip_Z = 6


actNameUSCHAD = {
    1:  'Walking Forward',
    2:  'Walking Left',
    3:  'Walking Right',
    4:  'Walking Upstairs',
    5:  'Walking Downstairs',
    6:  'Running Forward',
    7:  'Jumping Up',
    8:  'Sitting',
    9:  'Standing',
    10: 'Sleeping',
    11: 'Elevator Up',
    12: 'Elevator Down',
}


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
            trial = mat_file['sensor_readings'].astype('float64')

            self.add_info_data(act, subject, trial_id, trial, self.dir_save)
            #print('file_name:[{}] s:[{}]'.format(filepath, subject))

        self.save_data(self.dir_save)
