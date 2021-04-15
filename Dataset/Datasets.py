import numpy as np
import csv, sys, glob, os
import pandas as pd
from abc import ABCMeta, abstractmethod

#Comparar e salvar nome de atividades com os nomes padroes, por exemplo: Walk, walk, Wlk, salvar no arquivo como walk 

class Dataset(metaclass=ABCMeta):
    #
    # Comentários: Passar como parâmetro o diretorio de leitura e de salvamento do dataset
    #
    def __init__(self, name, dir_dataset, dir_save, freq = 100):
        self.name = name
        self.dir_dataset = dir_dataset
        self.dir_save = dir_save
        self.freq = freq
    
    #
    # Comentários: Função que salva arquivo intermediário igual
    #
    def save_file(self, act, subject, trial_id, trial, output_dir):
        output_file_name = '{}_s{}_t{}.txt'.format(act.lower(), subject, trial_id)
        output_file_name = output_dir+output_file_name

        np.savetxt(X=trial, fmt='%s', fname=output_file_name, delimiter=' ')
    

    #
    # Função deve ser implementada, utilizar o diretorio do dataset para ler todos os dados e salvar no formato (sensorA sensorB sensorC)
    #
    @abstractmethod
    def preprocess(self):
        pass

class Wisdm(Dataset):

    def preprocess(self):
        file_name = self.dir_dataset
        output_dir = ''
        separator = '_'
        idx_label = 1

        f = open(file_name)
        lines = f.readlines()
        iterator = 0
        trial = []
        trial_id = 0
        for line in lines:
            try:
                split = line.strip().split(',')
                subject, act, time_stamp, x, y, z = line.strip().split(',')

                #It is the same trial
                if iterator < len(lines)-1 and lines[iterator+1].split(',')[1] == act and lines[iterator+1].split(',')[0] == subject:
                        if time_stamp != '0': #timestamp equal to zero is a bug of the trial
                            trial.append((x, y, z))

                #The next line will be a novel trial
                else:
                    print('{} {} {}'.format(act, subject, trial_id))
                    self.save_file(act, subject, trial_id, trial, self.dir_save)
                    trial_id = trial_id + 1
            except:
                print('Erro :'+line)


class MHEALTH(Dataset):

    def preprocess(self):
        files = glob.glob(pathname='*.log')
        output_dir = '../output'

        subject = 0
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            for line in lines:
                split = line.strip().split('        ')
                columns = len(split)-1
                if len(split) < 24:
                    print('Error')

                act = split[columns]

                #It is the same trial
                if iterator != len(lines)-1 and lines[iterator+1].split('   ')[len(split)-1].replace('\n','') == act:
                    trial.append(split[0:columns])

                #The next line will be a novel trial
                else:
                    self.save_file(act, subject, trial_id, trial)
                    trial_id = trial_id + 1
                    trial = []

                iterator = iterator + 1
            print('file_name:[{}] s:[{}]'.format(file, subject))


class PAMAP2(Dataset):

    def preprocess(self):
        files = glob.glob(pathname='Optional/*.dat')
        output_dir = '../output/2'
        idx_label = 1
        subject = 0
        #remove_columns = [0, 1, 2, 3,  16, 17, 18, 19, 20, 33, 34, 35, 36, 37, 50, 51, 52, 53]#Without temperature
        remove_columns = [0, 1, 2, 16, 17, 18, 19, 33, 34, 35, 36, 50, 51, 52, 53]#With temperature
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            incorrect = 0
            for line in lines:
                split = line.strip().split(' ')
                sample =  np.asarray(split)
                act = sample[1]

                sample = np.delete(sample, remove_columns)

                #It is the same trial
                #lines[iterator + 1].split(' ')[1] is the next activity
                if iterator != len(lines)-1 and lines[iterator+1].split(' ')[1] == act:
                    idx = np.where(sample == 'NaN')[0]
                    if(idx.size==0):
                        trial.append(sample)
                    else:#Incorrect file
                        incorrect = incorrect+1

                #The next line will be a novel trial
                else:
                    self.save_file(act, subject, trial_id, trial)
                    trial_id = trial_id + 1
                    trial = []


                iterator = iterator + 1
            print('file_name:[{}] s:[{}]'.format(file, subject))
            print('{} incorrect lines in file {}'.format(str(incorrect), file))