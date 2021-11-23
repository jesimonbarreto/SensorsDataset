import numpy as np
import random
import os, pickle,glob
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold, train_test_split
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(0, '../')
from Signal.Transform import interpolate_sensors
from Utils.actTranslate import actNameVersions
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

    def set_name_act(self):
	    self.name_act = True

    def set_act_processed(self):
	    self.actSelected = []
	    for dtb in self.list_datasets:
		    aux = [v for i, v in dtb.activitiesDict.items()]
		    self.actSelected += list(map(lambda x: x.lower(), aux))

    def remove_subject(self, code):
	    pass

    def remove_action(self, selectedActivities=None, removeActivities=None):
	    # TODO: Lidar com as variações de nome de atividades
	    if selectedActivities:
		    #create a bigger list with all variations of each activty name
		    selectedActivities = list(map(lambda x: x.lower(), selectedActivities))
		    aux = [actNameVersions[i] for  i in selectedActivities if i in actNameVersions.keys()]
		    aux = [val for sublist in aux for val in sublist]
		    selectedActivities += aux
		    self.actSelected = selectedActivities
	    if removeActivities:
		    removeActivities = list(map(lambda x: x.lower(), removeActivities))
		    aux = [actNameVersions[i] for  i in removeActivities if i in actNameVersions.keys()]
		    removeActivities += aux
		    aux = self.actSelected
		    self.actSelected = []
		    for act in aux:
			    if act not in removeActivities:
				    self.actSelected.append(act)

    def add_consult_label(self, a):
        z = self.consult_label.copy()   # start with x's keys and values
        z.update(a)    # modifies z with y's keys and values & returns None
        self.consult_label = z.copy()

    # Split trial in samples
    def sw(self, trial=None, freq = None):
        r = 0
        delta = freq * self.time_wd
        output = []

        sample = np.squeeze(trial)

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
               #TODO: entender a funcionalidade do label generator
                #isso eh de fato necessario ? poderia usar o dicionario de atividades de cada dataset...

                if label not in self.activity.keys() and label in self.actSelected:
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
                act = file.split(self.separator)[self.idx_label]
                if idx not in self.subject.keys() and act in self.actSelected:
                    self.subject_idx = self.subject_idx + 1
                    self.subject[idx] = self.subject_idx
            
        return self.subject

    def data_generator(self, files, data_name, dir_input_file, freq_data, new_freq):
        count = {}
        for id_, fl in enumerate(files):
            pkl = os.path.join(dir_input_file, data_name+'_'+str(id_)+'.pkl')
            with open(pkl, 'rb') as handle:
                data = pickle.load(handle)
            fls = [i for i in data]
            for file in fls:
                label_ = file.split(self.separator)[self.idx_label]
                if label_ in self.actSelected:
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
                    if samples:
                        # remove samples with NaN
                        new_samples = []
                        for sample in samples:
                            array_sum = np.sum(sample)
                            array_has_nan = np.isnan(array_sum)
                            if not array_has_nan:
                                new_samples.append(sample)
                            else:
                                if label_ not in count:
                                    count[label_] = 1
                                else:
                                    count[label_] += 1
                        samples = new_samples
                    for i in range(0, len(samples)):
                        self.X.append(np.array([samples[i]]))
                        if self.name_act:
                            act_name = data_name+'-'+label_
                        else:
                            act_name = label_
                        self.y.append(act_name)
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
            Y[i, self.activity[y[i]]] = 1.
        return Y

    def simple_generate(self, dir_save_file, new_freq = 20,MultiDatasetName = None):

        if len(self.list_datasets) == 1:
            name_file = f'{self.list_datasets[0].name}_f{new_freq}_t{self.time_wd}'
        else:
            name_file = f'Multi_{MultiDatasetName}f{new_freq}_t{self.time_wd}'
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
            #y_categorical = _to_categorical(y_names, len(self.activity))
            np.savez_compressed(os.path.join(dir_save_file,name_file), X=self.X, y=self.y, folds=folds)
        
            print('Activities performed by less than 2 subjects:')
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
        self.name_sub = False
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
        count = {}
        for id_, fl in enumerate(files):
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

                    if samples:
                        if freq_data != new_freq:
                            type_interp = 'cubic'
                            try:
                                samples = interpolate_sensors(samples, type_interp, new_freq * self.time_wd)
                            except:
                                print('[Interpolation] Sample not used: size {}, local {}'.format(len(samples), file))
                        # remove samples with NaN
                        new_samples = []
                        for sample in samples:
                            array_sum = np.sum(sample)
                            array_has_nan = np.isnan(array_sum)
                            if not array_has_nan:
                                new_samples.append(sample)
                            else:
                                if label_ not in count:
                                    count[label_] = 1
                                else:
                                    count[label_] += 1
                        samples = new_samples

                        for i in range(0, len(samples)):
                            self.X.append(np.array([samples[i]]))
                            act_name = ''
                            if self.name_act:
                                act_name += data_name + '-'
                            if self.name_sub:
                                act_name += subject_idx_ + '-'

                            act_name += label_

                            self.y.append(act_name)
                            self.groups.append(subject_idx_)
                            self.fundamental_matrix[label][subject_idx_] += 1
                    #else:
                    #    print('[Trial crop] Sample not used: size {}, local {}'.format(len(samples), file))
        print(f'Done. \nNumber of samples per activity removed (NaN values).')
        for c, v in count.items():
            print(f'{c} - {v}')

    def set_name_act(self):
        self.name_act = True

    def set_name_sub(self):
        self.name_sub = True

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

        # divide training per dataset
        Xy_train = {}
        for xx, yy in zip(_X_train, _y_train):
            dataset_name = yy.split('-')[0]
            if dataset_name in Xy_train:
                Xy_train[dataset_name][0].append(np.squeeze(xx))
                Xy_train[dataset_name][1].append(yy)
            else:
                Xy_train[dataset_name] = [[xx], [yy]]

        return np.array([Xy_train]), np.array(X_test), np.array(y_test)

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
        counts = []
        act_name, count = np.unique(self.y, return_counts=True)
        for a, c in zip(act_name, count):
            if c <= n:
                acts.append(a)
                counts.append(c)

        return acts, counts

    def remove_activities(self, n):
        acts, cs = self.act_with_less_than_n_samples(n)
        act_to_remove = []
        counts = []
        for i in range(len(acts)):
            if acts[i] not in self.target_tasks:
                act_to_remove.append(acts[i])
                counts.append(cs[i])

        newXy = [[x, y] for x, y in zip(self.X, self.y) if y not in act_to_remove]
        newX = [x[0] for x in newXy]
        newY = [x[1] for x in newXy]
        self.X = newX
        self.y = newY

        print("Activities removed because of small number of samples\n\n")
        if act_to_remove:
            for i in range(len(act_to_remove)):
                print("{}-{}\n".format(act_to_remove[i], counts[i]))
        else:
            print("None")
        print("\n")

    def simple_generate(self, dir_save_file, new_freq=20):
        if len(self.list_datasets) == 1:
            name_file = '{}_f{}_t{}'.format(self.list_datasets[0].name, new_freq, self.time_wd)
        else:

            name_file = 'f{}_t{}_{}'.format(new_freq, self.time_wd, self.exp_name)

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

        # remove activities with less than n samples (necessary for 20-shot meta learning)
        self.remove_activities(199)

        self.X = np.array(self.X, dtype=float)
        self.y = np.array(self.y)

        # normalization [-0.5, 0.5]
        for dataset in tqdm(self.list_datasets, desc='Normalizing samples'):
            tmp = []
            for xx, yy in zip(self.X, self.y):
                # get all activities from a dataset
                if dataset.name in yy:
                    tmp.append(xx)
            # normalize each sample from a dataset using min max calculate using tmp
            for idx, yy in enumerate(self.y):
                if dataset.name in yy:
                    self.X[idx] = ((self.X[idx] - np.min(tmp)) / (np.max(tmp) - np.min(tmp))) - 0.5

        # Meta learning train and test splits for each few-shot scenario

        Xy_train, X_test, y_test = self.split_data()

        one_shot_kfold = self.get_k_fold(X_test, y_test, 1, 5)
        five_shot_kfold = self.get_k_fold(X_test, y_test, 5, 5)
        ten_shot_kfold = self.get_k_fold(X_test, y_test, 10, 5)
        twenty_shot_kfold = self.get_k_fold(X_test, y_test, 20, 5)
        no_shot_kfold = self.get_k_fold(X_test, y_test, -1, 5)

        np.savez_compressed(os.path.join(dir_save_file, name_file + "_FSL"),
                            Xy_train=Xy_train,
                            X_test=X_test, y_test=y_test,
                            kfold_1_shot=one_shot_kfold,
                            kfold_5_shot=five_shot_kfold,
                            kfold_10_shot=ten_shot_kfold,
                            kfold_20_shot=twenty_shot_kfold,
                            kfold_no_shot=no_shot_kfold)

        # print('Activities performed by less than 2 subjects')
        # for row in invalid_rows:
        #     print(row)

        return Xy_train, X_test, y_test


class MetaLoso(object):
    def __init__(self, list_datasets, dir_datasets, tasks_list, exp_name, overlapping=0.0, time_wd=5):

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
        self.name_sub = False
        self.exp_name = exp_name
        self.tasks_list = tasks_list

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
        count = {}
        for id_, fl in enumerate(files):
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

                    if samples:
                        if freq_data != new_freq:
                            type_interp = 'cubic'
                            try:
                                samples = interpolate_sensors(samples, type_interp, new_freq * self.time_wd)
                            except:
                                print(
                                    '[Interpolation] Sample not used: size {}, local {}'.format(len(samples), file))
                        # remove samples with NaN
                        new_samples = []
                        for sample in samples:
                            array_sum = np.sum(sample)
                            array_has_nan = np.isnan(array_sum)
                            if not array_has_nan:
                                new_samples.append(sample)
                            else:
                                if label_ not in count:
                                    count[label_] = 1
                                else:
                                    count[label_] += 1
                        samples = new_samples
                        for i in range(0, len(samples)):
                            self.X.append(np.array([samples[i]]))
                            act_name = ''
                            if self.name_act:
                                act_name += data_name + '-'
                            if self.name_sub:
                                act_name += str(subject_idx_) + '-'

                            act_name += label_

                            self.y.append(act_name)
                            self.groups.append(subject_idx_)
                            self.fundamental_matrix[label][subject_idx_] += 1
                    # else:
                    #    print('[Trial crop] Sample not used: size {}, local {}'.format(len(samples), file))
        print(f'Done. \nNumber of samples per activity removed (NaN values).')
        for c, v in count.items():
            print(f'{c} - {v}')

    def set_name_act(self):
        self.name_act = True

    def set_name_sub(self):
        self.name_sub = True

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

    def simple_generate(self, dir_save_file, new_freq=20):
        if len(self.list_datasets) == 1:
            name_file = '{}_f{}_t{}'.format(self.list_datasets[0].name, new_freq, self.time_wd)
        else:
            name_file = 'f{}_t{}_{}'.format(new_freq, self.time_wd, self.exp_name)

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

        self.X = np.array(self.X, dtype=float)
        self.y = np.array(self.y)

        _X, _y = [], []
        # filter only the most frequent activities
        for sample, label in zip(self.X, self.y):
            if any(label.split("-")[0] in tt for tt in self.tasks_list) and any(label.split("-")[2] in tt for tt in self.tasks_list):
                _X.append(sample)
                _y.append(label)

        self.X = _X
        self.y = _y

        subjects_used = []
        # verify if all subjects have the activities
        for d in self.list_datasets:
            tasks = [t for t in self.tasks_list if d.name in t]
            n_subjects = sorted([int(t.split("-")[1]) for t in np.unique(self.y) if d.name in t])[-1]
            for n in range(n_subjects):
                n_act_sub = [t for t in np.unique(self.y) if d.name in t and '-' + str(n) + '-' in t]
                use = True
                for ts in tasks:
                    if not any(ts.split("-")[-1] in tt for tt in n_act_sub):
                        use = False
                if use:
                    subjects_used.append(d.name + '-' + str(n))

        _X, _y = [], []
        # filter only the most frequent activities
        for sample, label in zip(self.X, self.y):
            d_a = label.split("-")[0] + "-" + label.split("-")[1]
            if d_a in subjects_used:
                _X.append(sample)
                _y.append(label)

        self.X = _X
        self.y = _y

        # normalization [-0.5, 0.5]
        for dataset in tqdm(self.list_datasets, desc='Normalizing samples'):
            tmp = []
            for xx, yy in zip(self.X, self.y):
                # get all activities from a dataset
                if dataset.name in yy:
                    tmp.append(xx)
            # normalize each sample from a dataset using min max calculate using tmp
            for idx, yy in enumerate(self.y):
                if dataset.name in yy:
                    self.X[idx] = ((self.X[idx] - np.min(tmp)) / (np.max(tmp) - np.min(tmp))) - 0.5

        np.savez_compressed(os.path.join(dir_save_file, name_file),
                            X=self.X, y=self.y)