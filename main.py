import numpy as np
import csv, sys, glob, os
import pandas as pd
from enum import Enum

from Dataset.Datasets import Wisdm
from Dataset.Datasets import MHEALTH
from Process.Protocol import Loso
from Dataset.Datasets import Sensors_MHEALTH as ss_mth


def preprocess_datasets(datasets):

    for dtb in datasets:
        #load and save file preprocess
        dtb.preprocess()


if __name__ == "__main__":
    
    #list_name_file = ['../','../']
    if len(sys.argv) > 2:
        file_wisdm = sys.argv[1]
        dir_datasets = sys.argv[2]
        dir_save_file = sys.argv[3]
    else:
        file_wisdm = '/home/jesimon/Documents/Project_sensors_dataset/wisdm/debug.txt'
        dir_datasets = '/home/jesimon/Documents/Project_sensors_dataset/dataset_preprocess/'
        dir_save_file = '/home/jesimon/Documents/Project_sensors_dataset/'
        
    
    #Creating dataset
    #name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    w = Wisdm('Wisdm', file_wisdm, dir_datasets, freq = 20, trial_per_file = 1000000)
    m = MHEALTH('Mhealth', file_wisdm, dir_datasets, freq = 20, trial_per_file = 1000000)
    
    signals_m = [ss_mth.acc_chest_X, ss_mth.acc_chest_Y] 
    m.set_signals_use(signals_m)

    
    #list datasets
    datasets = [w]
    preprocess_datasets(datasets)

    
    #Creating Loso evaluate generating
    generate_ev = Loso(datasets, overlapping = 0.0, time_wd=5)
    #function to save information e data
    #files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq = 20)
    
    #save a npz X = (n_samples, 1, freq*time, 3); y = [n_samples, n_classes] (,'walk','standing',...)