import numpy as np
import random
import os, pickle,glob
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold, train_test_split
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from Signal.Transform import interpolate_sensors
from tqdm import tqdm


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
        self.name_act = False

    def add_consult_label(self, a):
        z = self.consult_label.copy()   # start with x's keys and values
        z.update(a)    # modifies z with y's keys and values & returns None
        self.consult_label = z.copy()

    # Split trial in samples
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

    def cv_generator(self, y, n_folds=10):
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
                    try:
                        samples = interpolate_sensors(samples, type_interp, new_freq * self.time_wd)
                    except:
                        print('Sample not used: size {}, local {}'.format(len(samples),file))
                
                for i in range(0, len(samples)):
                    self.X.append(np.array([samples[i]]))
                    if self.name_act:
                        act_name = data_name+'-'+label_
                    else:
                        act_name = label_
                    self.y.append(act_name)
                    self.groups.append(subject_idx_)
                    self.fundamental_matrix[label][subject_idx_] += 1

    def set_name_act(self):
        self.name_act = True
    
    def remove_subject(self, code):
        pass

    def remove_action(self, code):
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
            Y[i, self.activity[y[i]]] = 1.
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

        try:
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
        except:
            print("[ERRO] Divisão em protocolo LOSO falhou. Verifique o número de classes do dataset!")


class MetaLearning(object):
    def __init__(self, list_datasets, dir_datasets, source_tasks, target_tasks, exp_name, overlapping=0.0, time_wd=5):
        self.list_datasets = list_datasets
        self.dir_datasets = dir_datasets
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
        self.name_act = False
        self.source_tasks = source_tasks
        self.target_tasks = target_tasks
        self.exp_name = exp_name

    def add_consult_label(self, a):
        z = self.consult_label.copy()  # start with x's keys and values
        z.update(a)  # modifies z with y's keys and values & returns None
        self.consult_label = z.copy()

    # Split trial in samples
    def sw(self, trial=None, freq=None):
        r = 0
        delta = freq * self.time_wd
        output = []

        sample = trial

        while r + delta < len(sample):
            block = sample[r:r + delta]
            output.append(block)
            r = r + delta
            r = r - (int(delta * self.overlapping))

        return output

    def subject_trials_and_label_generator(self, files):
        for pkl in files:
            with open(pkl, 'rb') as handle:
                data = pickle.load(handle)
                fl = [i for i in data.keys()]
                for file in fl:
                    idx = file.split(self.separator)[self.idx_subject]
                    if idx not in self.subject.keys():
                        self.subject_idx = self.subject_idx + 1
                        self.subject[idx] = self.subject_idx

                    label = file.split(self.separator)[self.idx_label]
                    if label not in self.activity.keys():
                        self.label_idx += 1
                        self.activity[label] = self.label_idx

        return self.subject, self.activity

    def data_generator(self, files, data_name, dir_input_file, freq_data, new_freq):

        print("\nAdding samples from {}".format(data_name), flush=True)
        for id_, fl in enumerate(tqdm(files)):
            pkl = os.path.join(dir_input_file, data_name + '_' + str(id_) + '.pkl')
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

                    trial = np.squeeze(np.array(data[file]))

                    samples = self.sw(trial=trial, freq=freq_data)

                    if freq_data != new_freq:
                        type_interp = 'cubic'
                        try:
                            samples = interpolate_sensors(samples, type_interp, new_freq * self.time_wd)
                        except:
                            print('Sample not used: size {}, local {}'.format(len(samples), file))

                    for i in range(0, len(samples)):
                        self.X.append(np.array([samples[i]]))
                        if self.name_act:
                            act_name = data_name + '-' + label_
                        else:
                            act_name = label_
                        self.y.append(act_name)
                        self.groups.append(subject_idx_)
                        self.fundamental_matrix[label][subject_idx_] += 1
        print("Done")

    def set_name_act(self):
        self.name_act = True

    def remove_subject(self, code):
        pass

    def remove_action(self, code):
        pass

    def _to_categorical(self, y, nb_classes=None):
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
            Y[i, self.activity[y[i]]] = 1.
        return Y

    def split_data(self):
        _X_train, X_test, _y_train, y_test = [], [], [], []

        for sample, label in zip(self.X, self.y):
            if label in self.source_tasks:
                _X_train.append(sample)
                _y_train.append(label)
            elif label in self.target_tasks:
                X_test.append(sample)
                y_test.append(label)

        X_train, X_val, y_train, y_val = train_test_split(np.array(_X_train), _y_train, test_size=0.2, random_state=42)

        return X_train, np.array(y_train), X_val, np.array(y_val), np.array(X_test), np.array(y_test)

    def get_n_random_sample_per_class(self, indexs, y, n_shots):
        classes = np.unique(y)
        n_classes = len(np.unique(y))
        samples_per_classe = []
        for c in classes:
            if np.count_nonzero(y[indexs] == c) < n_shots:
                sys.exit("There is no enough sample in this split for class {} and n_shot = {}".format(c, n_shots))
            samples = []
            while len(samples) < n_shots:
                idx = np.random.choice(indexs, 1)[0]
                if y[idx] == c:
                    samples.append(idx)
            samples_per_classe.extend(samples)
        #  check if each class has number of samples equal to n_shots
        if len(samples_per_classe) != n_classes * n_shots:
            sys.exit("Class/n_shots integrity failed. Expected shape:{} but get {}.".format(
                (n_classes * n_shots), len(samples_per_classe)))
        return samples_per_classe

    def get_k_fold(self, X, y, n_shots, n_folds):
        fold = []
        rskf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
        for train_index, test_index in rskf.split(X, y):
            if n_shots != -1:  # get only  k-shots from train
                train_index = self.get_n_random_sample_per_class(train_index, y, n_shots)
            fold.append({"train_idx": train_index, "test_idx": test_index})

        return fold

    def act_with_less_than_n_samples(self, n):
        acts = []
        act_name, count = np.unique(self.y, return_counts=True)
        for a, c in zip(act_name, count):
            if c < n:
                acts.append(a)
        return acts

    def remove_activities(self, n):
        act_to_remove = self.act_with_less_than_n_samples(n)

        newXy = [[x, y] for x, y in zip(self.X, self.y) if y not in act_to_remove]
        newX = [x[0] for x in newXy]
        newY = [x[1] for x in newXy]
        self.X = newX
        self.y = newY

    def simple_generate(self, dir_save_file, new_freq=20):
        if len(self.list_datasets) == 1:
            name_file = '{}_f{}_t{}'.format(self.list_datasets[0].name, new_freq, self.time_wd)
        else:

            name_file = 'Multi_f{}_t{}_{}'.format(new_freq, self.time_wd, self.exp_name)

        print("Reading pkl files...", flush=True)

        files_s = {}
        for id_, dtb in enumerate(self.list_datasets):
            files_s[dtb.name] = []
            input_dir = dtb.dir_save
            files = glob.glob(os.path.join(input_dir, '*.pkl'))
            for pkl in files:
                if os.path.split(pkl)[-1].split('_')[0] == dtb.name:
                    files_s[dtb.name].append(pkl)
            self.subject_trials_and_label_generator(files_s[dtb.name])
        print("Done.", flush=True)

        # Matrix Activity (row) by Subject (col)
        self.fundamental_matrix = np.zeros((len(self.activity), len(self.subject)))

        for id_, dtb in enumerate(self.list_datasets):
            input_dir = dtb.dir_save
            dataset_name = dtb.name
            self.data_generator(files_s[dataset_name], dataset_name, input_dir, dtb.freq, new_freq)
            # self.add_consult_label(dtb.labels)

        self.groups = np.array(self.groups)

        # remove activities with less than 10 samples (necessary for 5-shot meta learning)
        self.remove_activities(50)

        self.X = np.array(self.X, dtype=float)
        self.y = np.array(self.y)

        invalid_rows = []
        for row in self.fundamental_matrix:
            print(row)
            check_zeros = np.where(row != 0.)
            if check_zeros[0].shape[0] < 2:  # An activity is  performed just by one subject
                invalid_rows.append(row)

        # Meta learning train and test splits for each few-shot scenario

        X_train, y_train, X_val, y_val, X_test, y_test = self.split_data()

        one_shot_kfold = self.get_k_fold(X_test, y_test, 1, 5)
        five_shot_kfold = self.get_k_fold(X_test, y_test, 5, 5)
        ten_shot_kfold = self.get_k_fold(X_test, y_test, 10, 5)
        twenty_shot_kfold = self.get_k_fold(X_test, y_test, 20, 5)
        no_shot_kfold = self.get_k_fold(X_test, y_test, -1, 5)

        np.savez_compressed(os.path.join(dir_save_file, name_file + "_FSL"),
                            X_train=X_train, y_train=y_train,
                            X_test=X_test, y_test=y_test,
                            X_val=X_val, y_val=y_val,
                            kfold_1_shot=one_shot_kfold,
                            kfold_5_shot=five_shot_kfold,
                            kfold_10_shot=ten_shot_kfold,
                            kfold_20_shot=twenty_shot_kfold,
                            kfold_no_shot=no_shot_kfold)

        print('Activities performed by less than 2 subjects')
        for row in invalid_rows:
            print(row)
        # except:
        #     sys.exit("[ERRO] Divisão em protocolo LOSO falhou. Verifique o número de classes do dataset!")