import pickle
import sys
from abc import ABCMeta, abstractmethod

import numpy as np
import pandas as pd
from scipy.io import loadmat
import random
import csv


#Class name pattern - use gerund with the first capital letter
#Examples: Walking, Standing, Upstairs
#TODO create a file with all activities already used 
class Dataset(metaclass=ABCMeta):
    #
    # Comentários: Passar como parâmetro o diretorio de leitura e de salvamento do dataset
    #
    def __init__(self, name, dir_dataset, dir_save, freq = 100, trials_per_file=100000):
        self.name = name
        self.dir_dataset = dir_dataset
        self.dir_save = dir_save
        self.freq = freq
        self.data = {}
        # Quando tiver n_save_file trial id em data, sera salvo em disco e os data sera limpado
        self.trials_per_file = trials_per_file
        self.n_pkl = 0
        self.labels = {}
        self.signals_use = []
    
    #
    # Comentários: Função que salva arquivo intermediário igual
    #
    def save_file(self, act, subject, trial_id, trial, output_dir):
        output_file_name = '{}_s{}_t{}.txt'.format(act.lower(), subject, trial_id)
        output_file_name = output_dir+output_file_name

        np.savetxt(X=trial, fmt='%s', fname=output_file_name, delimiter=' ')
    
    def set_signals_use(self, signals):
        for s in signals:
            self.signals_use.append(s)
    
    def get_signals_use(self):
        return self.signals_use

    def add_info_data(self, act, subject, trial_id, trial, output_dir):
        output_name = '{}_s{}_t{}'.format(act.lower(), subject, trial_id)
        self.data[output_name] = trial
        if trial_id % self.trials_per_file == 0 and trial_id != 0:
            try:
                with open(output_dir+self.name+'_'+str(self.n_pkl)+'.pkl', 'wb') as handle:
                    pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.data = {}
                self.n_pkl += 1
            except:
                sys.exit('Erro save pickle {} for {} dataset'.format(self.n_pkl, self.name))

    def save_data(self, output_dir):
        try:
            with open(output_dir+self.name+'_'+str(self.n_pkl)+'.pkl', 'wb') as handle:
                pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.data = {}
            self.n_pkl += 1
        except:
            sys.exit('Erro save pickle {} for {} dataset'.format(self.n_pkl, self.name))

    def add_label_class(self, code, label):
        self.labels[code] = label


    """
    Funções que devem ser implementadas, utilizar o diretorio do dataset para ler
    todos os dados e salvar no formato (sensorA sensorB sensorC)
    """

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def print_info(self):
        pass
