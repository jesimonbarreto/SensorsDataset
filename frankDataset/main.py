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
from Process.Manager import preprocess_datasets
from Dataset.Datasets import Wisdm
from Dataset.cook import cook2020
from Dataset.Nonsense19 import NonSense
from Process.Protocol import Loso


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
        file ='C:\\Users\\gcram\\Documents\\Smart Sense\\NewDatasetPool\\cookRaw\\'
        file_pm = '/home/jesimon/Documents/others/datasets/PAMAP2_Dataset/'
        dir_save_file = 'C:\\Users\\gcram\\Documents\\Smart Sense\\NewDatasetPool\\cookRaw\\testOutput\\'
	    
        
    
    #Creating datasets
    #name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    w = Wisdm('Wisdm', file_wisdm, dir_datasets, freq = 20, trials_per_file = 1000000)
    utd = UTDMHAD1('UTD1', file_utd1, dir_datasets, freq = 50, trials_per_file = 1000000)
    p2 = PAMAP2('Pamap2', file_pm, dir_datasets, freq = 50, trials_per_file = 10000)
    mh = MHEALTH('Mhealth', file_mh, dir_datasets, freq = 100, trials_per_file = 10000)

    #Define signals of each dataset
    #sig_w = [sw.acc_front_pants_pocket_X, sw.acc_front_pants_pocket_Y, sw.acc_front_pants_pocket_Z]
    #w.set_signals_use(sig_w)

    #sig_utd = [su.acc_hand_X, su.acc_hand_Y, su.acc_hand_Z]
    #utd.set_signals_use(sig_utd)

    sig_pm = [sp.acc1_dominant_wrist_X, sp.acc1_dominant_wrist_Y, sp.acc1_dominant_wrist_Z]
    p2.set_signals_use(sig_pm)
    
    #sig_m = [sm.acc_chest_X, sm.acc_chest_Y, sm.acc_chest_Z]
    #mh.set_signals_use(sig_m)
    
    #list datasets
    datasets = [p2]

    #preprocessing
    preprocess_datasets(datasets)
    
    #Creating Loso evaluate generating
    generate_ev = Loso(datasets, overlapping = 0.0, time_wd=5)
    #Save name of dataset in variable y
    generate_ev.set_name_act()
    #function to save information e data
    #files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq = 20)
    


