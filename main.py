import numpy as np
import csv, sys, glob, os
import pandas as pd

from Dataset.Datasets import Wisdm
from Process.Protocol import Loso

#load format of each dataset for dic['person']['activity']['sensors'] = np.array(samples,axis)

def preprocess_datasets(datasets):

    for dtb in datasets:
        #load and save file preprocess
        dtb.preprocess()


if __name__ == "__main__":
    
    #list_name_file = ['../','../']
    file_wisdm = '/home/jesimon/Documents/Project_sensors_dataset/wisdm/WISDM_ar_v1.1_raw.txt'
    dir_datasets = '/home/jesimon/Documents/Project_sensors_dataset/dataset_preprocess/wisdm/'
    file_save = '/home/jesimon/Documents/Project_sensors_dataset/dataset_preprocess/wisdm_loso'
    
    #Creating dataset
    w = Wisdm('Wisdm',file_wisdm, dir_datasets)
    #list datasets
    datasets = [w]
    preprocess_datasets(datasets)
    
    #Creating Loso evaluate generating
    generate_ev = Loso(datasets, 100, 1)
    #function to save information e data
    generate_ev.simple_generate(file_save, idx_subject = 1, idx_label = 0, separator = '_', sw_size=100)
    