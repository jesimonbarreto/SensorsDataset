import numpy as np
import random
import os
from sklearn.model_selection import LeaveOneGroupOut
#from USCHAD_labelmap import activity2idx

class Loso(object):
    def __init__(self, list_datasets, time_wd, freq):
        self.list_datasets = list_datasets
        self.time_wd = time_wd
        self.freq = freq
        self.activity = {}
        self.label_idx = -1
        self.subject = {}
        self.subject_idx = -1
        self.overlapping = 0.5
        self.X = []
        self.y = []
        self.groups = []
        self.fundamental_matrix = []
        self.sw_size = 500
        self.separator = '_'
        self.idx_label = 1
        self.idx_subject = 0



    #Split trial in samples
    def sw(self, trial=None, size=None, overlapping=None):
        r = 0
        delta = size
        output = []

        sample = trial

        while r+delta < len(sample):
            block = sample[r:r+delta]
            output.append(block)
            r = r+delta
            r = r- (int(delta*overlapping))

        return output

    def cv_generator(self,y, n_folds=10):
        from sklearn.cross_validation import StratifiedKFold
        skf = StratifiedKFold(y, n_folds, shuffle=True)
        folds = []
        for i, (train_idx, test_idx) in enumerate(skf):
            folds.append((train_idx, test_idx))
        return folds

    def label_generator(self, files, idx_label):
        #self.label_idx = -1
        for file in files:
            label = file.split(self.separator)[idx_label]#[1:]#USCHAD
            if label not in self.activity.keys():
                self.label_idx += 1
                self.activity[label] = self.label_idx

        return self.activity

    def subject_trials(self,files, idx_subject):
        #subject = {}
        #subject_idx = -1
        for file in files:
            idx = file.split(self.separator)[idx_subject]#[-2:]
            #idx = file.split("_")[idx_subject][7:] #USCHAD
            if idx not in self.subject.keys():
                self.subject_idx = self.subject_idx + 1
                self.subject[idx] = self.subject_idx
        
        return self.subject

    def data_generator(self,files, input_file, freq_data):

        for file in files:
            label_ = file.split(self.separator)[self.idx_label]
            subject_ = file.split("_")[self.idx_subject]
            label = self.activity[label_] #list(self.activity.keys())[list(self.activity.values()).index(self.label_idx-1)]
            subject_idx_ = self.subject[subject_]

            file_name = '{}/{}'.format(input_file, file)
            
            trial = np.genfromtxt(file_name, delimiter=' ', filling_values=np.nan,
                                case_sensitive=True, deletechars='',replace_space=' ')

            samples = self.sw(trial=trial, size=self.sw_size, overlapping=self.overlapping)
            
            for i in range(0, len(samples)):
                ##passa a samples[i] com a quantidade de pontos que deve ter e pega a quantidade que ele tem faz o calculo
                #if self.freq != freq_data:
                #    diff = abs(self.freq - freq_data) * self.time_wd
                #    #chama function transformation to pass a sample for the value 
                #    #funcInterpola
                self.X.append([samples[i]])
                self.y.append(label)
                self.groups.append(subject_idx_)
                self.fundamental_matrix[label][subject_idx_] += 1


    def _to_categorical(self,y, nb_classes=None):
        '''Convert class vector (integers from 0 to nb_classes)
        to binary class matrix, for use with categorical models
        '''
        if not nb_classes:
            if 0 in y:
                nb_classes = np.max(y) + 1
            else:
                nb_classes = np.max(y)
        Y = np.zeros((len(y), nb_classes))
        for i in range(len(y)):
            Y[i, activity[y[i]]] = 1.
        return Y

    def example(self):
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([1, 2, 1, 2])
        groups = np.array([1, 1, 2, 3])
        logo = LeaveOneGroupOut()
        logo.get_n_splits(X, y, groups)
        for train_index, test_index in logo.split(X, y, groups):
            print("TRAIN:", train_index, "TEST:", test_index)

    def simple_generate(self, file_save, idx_subject = 1, idx_label = 0, separator = '_', sw_size=500):
        #TODO example()
        #input_dir = 'Z:/Pesquisa/benchmark_sensores/USC-HAD/output'
        file_name = file_save #'USC-HAD_loso'
        self.separator = separator
        self.idx_label = idx_label
        self.idx_subject = idx_subject
        self.sw_size = sw_size


        for id_, dtb in enumerate(self.list_datasets):
            input_dir = dtb.dir_save
            files = os.listdir(input_dir)
            #activity is the dictionary of the activities and index.
            self.label_generator(files, idx_label)
            #individuals_id is the dictionary of the subjects and subjects index 
            self.subject_trials(files, idx_subject)
            
        self.fundamental_matrix = np.zeros((len(self.activity),len(self.subject)))#Matrix Activity (row) by Subject (col)
        
        for id_, dtb in enumerate(self.list_datasets):
            input_dir = dtb.dir_save
            files = os.listdir(input_dir)
            self.data_generator(files, input_dir, dtb.freq)

        self.group = np.array(self.group)
        self.X = np.array(self.X)
        self.y = np.array(self.y)

        invalid_rows = []
        for row in self.fundamental_matrix:
            ###Apresentar o dataset de erro - falta implementar
            print(row)
            check_zeros = np.where(row != 0.)
            if check_zeros[0].shape[0] < 2: #An activity is performed just by one subject
                invalid_rows.append(row)

        if(len(invalid_rows) == 0):
            loso = LeaveOneGroupOut()
            tmp = loso.split(X=self.X, y=self.y, groups=self.groups)
            folds =[]
            for train_index, test_index in loso.split(self.X, self.y, self.groups):
                folds.append((train_index, test_index))

            self.X = np.array(self.X)
            y_names = np.array(self.y)
            self.y = _to_categorical(y_names, len(self.activity))
            np.savez_compressed(file_name, X=self.X, y=self.y, activities=self.activity, folds=folds)

        else:
            print('Problem at lines')
            for row in invalid_rows:
                print(row)


            