import numpy as np
import random
import os, pickle,glob
from sklearn.model_selection import LeaveOneGroupOut

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from Signal.Transform import interpolate_sensors

class Loso(object):
    def __init__(self, list_datasets, overlapping = 0.0, time_wd=5):
        self.list_datasets = list_datasets
        self.time_wd = time_wd
        self.activity = {}
        self.label_idx = -1
        self.subject = {}
        self.subject_idx = -1
        self.overlapping = overlapping
        self.X = []
        self.y = []
        self.groups = []
        self.fundamental_matrix = []
        self.separator = '_'
        self.idx_label = 0
        self.idx_subject = 1
        self.consult_label = {}

    def add_consult_label(self, a):
        z = self.consult_label.copy()   # start with x's keys and values
        z.update(a)    # modifies z with y's keys and values & returns None
        self.consult_label = z.copy()

    #Split trial in samples
    def sw(self, trial=None, freq = None):
        r = 0
        delta = freq * self.time_wd
        output = []

        sample = trial

        while r+delta < len(sample):
            block = sample[r:r+delta]
            output.append(block)
            r = r+delta
            r = r- (int(delta*self.overlapping))

        return output

    def cv_generator(self,y, n_folds=10):
        from sklearn.cross_validation import StratifiedKFold
        skf = StratifiedKFold(y, n_folds, shuffle=True)
        folds = []
        for i, (train_idx, test_idx) in enumerate(skf):
            folds.append((train_idx, test_idx))
        return folds

    def label_generator(self, files):
        #self.label_idx = -1
        for pkl in files:
            with open(pkl, 'rb') as handle:
                data = pickle.load(handle)
            fl = [i for i in data.keys()]
            for file in fl:
                label = file.split(self.separator)[self.idx_label]#[1:]#USCHAD
                if label not in self.activity.keys():
                    self.label_idx += 1
                    self.activity[label] = self.label_idx

        return self.activity

    def subject_trials(self,files):
        #subject = {}
        #subject_idx = -1
        for pkl in files:
            with open(pkl, 'rb') as handle:
                data = pickle.load(handle)
            fl = [i for i in data.keys()]
            for file in fl:
                idx = file.split(self.separator)[self.idx_subject]#[-2:]
                #idx = file.split("_")[idx_subject][7:] #USCHAD
                if idx not in self.subject.keys():
                    self.subject_idx = self.subject_idx + 1
                    self.subject[idx] = self.subject_idx
            
        return self.subject

    def data_generator(self, files, data_name, dir_input_file, freq_data, new_freq):

        for id_, fl in enumerate(files):
            pkl = os.path.join(dir_input_file, data_name+'_'+str(id_)+'.pkl')
            with open(pkl, 'rb') as handle:
                data = pickle.load(handle)
            fl = [i for i in data]
            for file in fl:
                label_ = file.split(self.separator)[self.idx_label]
                if len(self.consult_label) > 0:
                    label_ = self.consult_label[label_]
                subject_ = file.split("_")[self.idx_subject]
                label = self.activity[label_]
                subject_idx_ = self.subject[subject_]
                
                trial = data[file]
                
                samples = self.sw(trial = trial, freq = freq_data)

                if freq_data != new_freq:
                    type_interp = 'cubic'
                    samples = interpolate_sensors(samples, type_interp, new_freq * self.time_wd)
                
                for i in range(0, len(samples)):
                    self.X.append([samples[i]])
                    self.y.append(label_)
                    self.groups.append(subject_idx_)
                    self.fundamental_matrix[label][subject_idx_] += 1

    def remove_subject(code):
        pass
    def remove_action(code):
        pass

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

    def simple_generate(self, dir_save_file, new_freq = 20):
        if len(self.list_datasets) == 1:
            name_file = '{}_f{}_t{}'.format(self.list_datasets[0].name, new_freq, self.time_wd)
        else:
            name_file = 'Multi_f{}_t{}'.format(new_freq, self.time_wd)
        files_s = {}
        for id_, dtb in enumerate(self.list_datasets):
            files_s[dtb.name] = []
            input_dir = dtb.dir_save
            files = glob.glob(os.path.join(input_dir,'*.pkl'))
            for pkl in files:
                if os.path.split(pkl)[-1].split('_')[0] == dtb.name:
                    files_s[dtb.name].append(pkl)
                    #with open(pkl, 'rb') as handle:
                    #    data = pickle.load(handle)
                    #files_s[id_].append([i for i in data.keys()])
            self.label_generator(files_s[dtb.name])
            self.subject_trials(files_s[dtb.name])
        
        #Matrix Activity (row) by Subject (col)    
        self.fundamental_matrix = np.zeros((len(self.activity),len(self.subject)))
        
        for id_, dtb in enumerate(self.list_datasets):
            input_dir = dtb.dir_save
            dataset_name = dtb.name
            self.data_generator(files_s[dataset_name],dataset_name, input_dir, dtb.freq, new_freq)
            #self.add_consult_label(dtb.labels)

        self.groups = np.array(self.groups)
        self.X = np.array(self.X)
        #self.y = np.array(self.y)

        invalid_rows = []
        for row in self.fundamental_matrix:
            print(row)
            check_zeros = np.where(row != 0.)
            if check_zeros[0].shape[0] < 2: #An activity is performed just by one subject
                invalid_rows.append(row)

        #if(len(invalid_rows) == 0):
        loso = LeaveOneGroupOut()
        tmp = loso.split(X=self.X, y=self.y, groups=self.groups)
        folds =[]
        for train_index, test_index in loso.split(self.X, self.y, self.groups):
            folds.append((train_index, test_index))

        self.X = np.array(self.X)
        y_names = np.array(self.y)
        #self.y = _to_categorical(y_names, len(self.activity))
        np.savez_compressed(os.path.join(dir_save_file,name_file), X=self.X, y=self.y, folds=folds)
    
        print('Activities performed by less than 2 subjects')
        for row in invalid_rows:
            print(row)