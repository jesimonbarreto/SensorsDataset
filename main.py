import numpy as np
import csv, sys, glob, os
import pandas as pd
from Dataset.Datasets import Wisdm
from Dataset.cook import cook2020
from Dataset.Nonsense19 import NonSense
from Process.Protocol import Loso
from Signal.Transform import interpolate_sensors


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
        #file_wisdm = '/home/jesimon/Documents/Project_sensors_dataset/wisdm/debug.txt'
        #dir_datasets = '/home/jesimon/Documents/Project_sensors_dataset/dataset_preprocess/'
        #dir_save_file = '/home/jesimon/Documents/Project_sensors_dataset/'
        file ='C:\\Users\\gcram\\Documents\\Smart Sense\\NewDatasetPool\\19NonSense\\'
        dir_datasets = 'C:\\Users\\gcram\\Documents\\Smart Sense\\NewDatasetPool\\19NonSense\\'
        dir_save_file = 'C:\\Users\\gcram\\Documents\\Smart Sense\\NewDatasetPool\\19NonSense\\testOutput\\'
	    
        
    
    #Creating dataset
    #name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    #w = Wisdm('Wisdm', file_wisdm, dir_datasets, freq = 20, trial_per_file = 1000000)
    #dat = cook2020("Cook",file, dir_datasets, freq = 50, trial_per_file = 1000000)
    dat = NonSense("Nonsense19", file, dir_datasets, freq=50, trial_per_file=1000000)
    #list datasets
    datasets = [dat]
    preprocess_datasets(datasets)
    
    #Creating Loso evaluate generating

    generate_ev = Loso(datasets, overlapping = 0.0, time_wd=5)
    #function to save information e data
    #files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq = 20)
    
    #save a npz X = (n_samples, 1, freq*time, 3); y = [n_samples, n_classes] (,'walk','standing',...)