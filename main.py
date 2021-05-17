import numpy as np
import csv, sys, glob, os
import pandas as pd
from enum import Enum
from Dataset.Wisdm import Wisdm
from Dataset.Wisdm import SignalsWisdm as sw
from Dataset.Utdmhad1 import UTDMHAD1
from Dataset.Utdmhad1 import SignalsUtdmhad1 as su
from Dataset.Mhealth import MHEALTH
from Dataset.Mhealth import SignalsMHEALTH as sm
from Dataset.Pamap2 import PAMAP2
from Dataset.Pamap2 import SignalsPAMAP2 as sp

from Process.Protocol import Loso

def preprocess_datasets(datasets):
    #devem ser igual
    num_dim_signals = -1
    for dtb in datasets:
        if num_dim_signals == -1:
            num_dim_signals = len(dtb.get_signals_use())
        else:
            if num_dim_signals != len(dtb.get_signals_use()):
                print('[ERRO] - Todos os datasets que serão unidos devem ter o mesmo número sinais')
                sys.exit()

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
        dir_save_file = '/home/jesimon/Documents/Project_sensors_dataset/dataset_generated/'
        file_utd1 = '/home/jesimon/Documents/others/datasets/Inertial/'
        file_pm = '/home/jesimon/Documents/others/datasets/PAMAP2_Dataset/Optional/'
        file_mh = '/home/jesimon/Documents/others/datasets/MHEALTHDATASET/'
    
    #Creating dataset
    #name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    w = Wisdm('Wisdm', file_wisdm, dir_datasets, freq = 20, trials_per_file = 1000000)
    utd = UTDMHAD1('UTD1', file_utd1, dir_datasets, freq = 50, trials_per_file = 1000000)
    p2 = PAMAP2('Pamap2', file_pm, dir_datasets, freq = 50, trials_per_file = 10000)
    mh = MHEALTH('Mhealth', file_mh, dir_datasets, freq = 100, trials_per_file = 10000)

    sig_w = [sw.acc_hand_X, sw.acc_hand_Y, sw.acc_hand_Z] 
    w.set_signals_use(sig_w)

    sig_utd = [su.acc_hand_X, su.acc_hand_Y, su.acc_hand_Z]
    utd.set_signals_use(sig_utd)

    sig_pm = [sp.acc1_hand_X, sp.acc1_hand_Y, sp.acc1_hand_Z]
    p2.set_signals_use(sig_pm)
    
    sig_m = [sm.acc_chest_X, sm.acc_chest_Y, sm.acc_chest_Z]
    mh.set_signals_use(sig_m)
    #list datasets
    datasets = [mh]

    #preprocess_datasets(datasets)
    
    #Creating Loso evaluate generating
    generate_ev = Loso(datasets, overlapping = 0.0, time_wd=5)
    #function to save information e data
    #files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq = 50)
    


