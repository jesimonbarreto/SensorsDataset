from .Datasets import Dataset
import os
import pandas as pd
import zipfile
import glob
import csv
import random
import numpy as np
from enum import Enum


class SignalsCOOK(Enum):
    sensor_X = 0
    sensor_Y = 1
    sensor_Z = 2


actNameCOOK = {
    1: 'Activity 1',
    2: 'Activity 2',
    3: 'Activity 3'
}

class Cook2020(Dataset):
    # https://abc-research.github.io/cook2020/
    def print_info(self):
        return """
                device: 
                frequency: 
                positions: 
                sensors: 
                """

    def preprocess(self, sensor_list =  ['left_hip' ,'left_wrist' ,'right_arm' ,'right_wrist']):
        def parse_IMU(parent_dir, sub_dirs, startTime, endTime, file_name, window_length):
            data = []
            data_count = 0
            for sub_dir in sub_dirs:
                channel = []
                for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_name)):
                    file = open(fn, newline='')
                    reader = csv.reader(file)
                    first = True
                    count = 0
                    for row in reader:
                        if first:
                            first = False
                            continue
                        try:
                            timestamp = float(row[3])  # 4th column is timestamp
                        except:
                            row = row[0].split(';')
                            timestamp = float(row[3])
                        window_jitter1 = random.randint(-150, 150)
                        window_jitter2 = random.randint(-150, 150)
                        if (startTime + window_jitter1) <= timestamp <= (
                                endTime + window_jitter2) and count < window_length:

                            try:
                                channel.append([float(row[0]), float(row[1]), float(row[2])])
                            except:
                                continue
                            count = count + 1
                            data_count = data_count + 1
                data.append(channel)
            return data, data_count
        # merge train and test first!


#		zip_train = zipfile.ZipFile(os.path.join(self.dir_dataset,'train.zip'))
#		zip_train.extractall(self.dir_dataset)
#		zip_test = zipfile.ZipFile(os.path.join(self.dir_dataset,'test.zip'))
#		zip_test.extractall(self.dir_dataset)
#		zip_train.close()
#		zip_test.close()

        #get The labels:
        # read the labels
        testLabels = os.path.join(self.dir_dataset, 'test-labels.csv')
        testLabels = pd.read_csv(testLabels, sep=';',  header=[0, 1]).iloc[:, 0:2]
        testLabels.columns = ['idx','act']

        trainLabels = pd.read_csv(os.path.join(self.dir_dataset,'train','labels.txt'), delimiter = "\t",sep = ',')
        trainLabels.columns = ['act']
        trainLabels = trainLabels['act'].str.split(',',expand = True).iloc[:,0:2]
        trainLabels.columns = ['idx','act']

        labels = pd.concat([trainLabels, testLabels], axis=0)
        labels = labels.set_index('idx')

        min_data_count = 100
        sub_dirs = sensor_list

        number_of_samples = 500

        trial_id_ = dict()
        trial_id_['1'] = 0
        trial_id_['2'] = 0
        trial_id_['3'] = 0
        trial_id_['4'] = 0


        for part in ['train','test']:
            path =os.path.join(self.dir_dataset,part)
            file = os.listdir(os.path.join(path, sub_dirs[0]))

            for f in file:

                st_index = 0
                end_index = 30000
                step = 1000  # overlapping window, step
                window_index = 10000  # 6 second window
                f_name = f.split('.')[0]

                if f_name not in pd.unique(labels.index):
                    continue

                curr_label_file = labels.loc[f_name].values[0]
                curr_subject = f_name.split('_')[0][-1]
                while st_index + step < end_index:

                    data, data_count = parse_IMU(path, sub_dirs, st_index, st_index + window_index, f,
                                                 number_of_samples)
                    st_index = st_index + step

                    if data_count < min_data_count:
                        continue


                    train_data_sample = np.zeros((len(sensor_list ) *3, number_of_samples))
                    train_data_label = curr_label_file
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            train_data_sample[i * 3, j] = data[i][j][0]
                            train_data_sample[i * 3 + 1, j] = data[i][j][1]
                            train_data_sample[i * 3 + 2, j] = data[i][j][2]
                    trial = np.transpose(train_data_sample, (1, 0))
                    # trial = np.expand_dims(act, axis=0)
                    act = train_data_label[0].upper() + train_data_label[1:]
                    trial_id = trial_id_[curr_subject]
                    trial = train_data_sample
                    self.add_info_data(act, curr_subject ,trial_id , trial, self.dir_save)
                    trial_id_[curr_subject] += 1
        self.save_data(self.dir_save)