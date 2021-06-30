import numpy as np
import csv, sys, glob, os
import pandas as pd
from enum import Enum
from Dataset.Wisdm import WISDM
from Dataset.Wisdm import SignalsWisdm as sw
from Dataset.Utdmhad1 import UTDMHAD1
from Dataset.Utdmhad1 import SignalsUtdmhad1 as su
from Dataset.Mhealth import MHEALTH
from Dataset.Mhealth import SignalsMHEALTH as smh
from Dataset.Pamap2 import PAMAP2
from Dataset.Pamap2 import SignalsPAMAP2 as sp
from Process.Manager import preprocess_datasets
from Dataset.Cook2020 import COOK
from Dataset.Nonsense19 import NONSENSE

from Dataset.Ucihar import UCIHAR
from Dataset.Ucihar import SignalsUCIHAR as sig_uci

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
        #file_pm = '/home/jesimon/Documents/others/datasets/PAMAP2_Dataset/'
        file_p2 ='C:\\Users\\gcram\\Documents\\Smart Sense\\Datasets\\originals\\PAMAP2\\'
        file_mh = 'C:\\Users\\gcram\\Documents\\Smart Sense\\Datasets\\originals\\MHEALTHDATASET'
        file = 'C:\\Users\\gcram\\Documents\\Smart Sense\\Datasets\\originals\\uci-human-activity-recognition\\'
        savePath = 'C:\\Users\\gcram\\Documents\\Smart Sense\\Datasets\\frankDataset\\'
        
    
    #Creating datasets
    #name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    #w = Wisdm('Wisdm', file_wisdm, dir_datasets, freq = 20, trials_per_file = 1000000)
    #utd = UTDMHAD1('UTD1', file_utd1, dir_datasets, freq = 50, trials_per_file = 1000000)
    p2 = PAMAP2('Pamap2', file_p2, savePath, freq = 100, trials_per_file = 10000)
    #usc = USCHAD('Uschad',file_usc,savePath,freq = 100, trials_per_file = 10000)
    mh = MHEALTH('Mhealth', file_mh, savePath, freq = 100, trials_per_file = 10000)
    uci = UCIHAR('Ucihar',file,savePath,freq = 50,trials_per_file = 10000)
    

    #Define signals of each dataset
    #sig_w = [sw.acc_front_pants_pocket_X, sw.acc_front_pants_pocket_Y, sw.acc_front_pants_pocket_Z]
    #w.set_signals_use(sig_w)

    #sig_mh = [smh.acc_right_lower_arm_X, smh.acc_right_lower_arm_Y, smh.acc_right_lower_arm_Z]
    #mh.set_signals_use(sig_mh)
    #sig_pm = [sp.acc1_dominant_wrist_X, sp.acc1_dominant_wrist_Y, sp.acc1_dominant_wrist_Z]
    #p2.set_signals_use(sig_pm)
    uci.set_signals_use(sig_uci)
    
    #list datasets
    datasets = [uci]

    #preprocessing
    preprocess_datasets(datasets)
    
    #Creating Loso evaluate generating
    generate_ev = Loso(datasets, overlapping = 0.5, time_wd=5)
    #Save name of dataset in variable y
    generate_ev.set_name_act()
    #function to save information e data
    #files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(savePath, new_freq = 20)
    


