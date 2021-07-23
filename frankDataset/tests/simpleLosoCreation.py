import csv, sys, glob, os, json
sys.path.insert(0,'../')

import numpy as np
import pandas as pd
from enum import Enum

import argparse
from Dataset import Datasets
from Dataset.Ucihar import UCIHAR, SignalsUcihar
from Dataset.Dsads import DSADS, SignalsDsads
from Dataset.Uschad import USCHAD, SignalsUschad
from Dataset.Pamap2 import PAMAP2, SignalsPamap2

from Process.Manager import preprocess_datasets
from Process.Protocol import Loso


#defining the source and output directories
inPath = os.path.abspath('C:\\Users\\gcram\\Documents\\Smart Sense\\Datasets\\')
#outPath = os.path.realpath('results')
source = os.path.join(inPath, 'originals')
outPath = os.path.join(inPath, 'frankDataset/')
datasets = []
#
#Creating datasets objects:
pamaFile = os.path.join(source, 'PAMAP2')
p2 = PAMAP2('Pamap2', pamaFile, outPath, freq=100, trials_per_file=10000)
sig_pm = [SignalsPamap2.acc1_chest_X, SignalsPamap2.acc1_chest_Y, SignalsPamap2.acc1_chest_Z]
sig_pm += [SignalsPamap2.gyr_chest_X, SignalsPamap2.gyr_chest_Y, SignalsPamap2.gyr_chest_Z]
p2.set_signals_use(sig_pm)
datasets.append(p2)


dsaFile = os.path.join(source, 'uci-daily-and-sports-activities')
dsa = DSADS('Dsads', dsaFile, outPath, freq=25, trials_per_file=10000)
sig_dsa = [SignalsDsads.acc_torso_X, SignalsDsads.acc_torso_Y, SignalsDsads.acc_torso_Z]
sig_dsa += [SignalsDsads.gyr_torso_X, SignalsDsads.gyr_torso_Y, SignalsDsads.gyr_torso_Z]
dsa.set_signals_use(sig_dsa)
datasets.append(dsa)

uscFile = os.path.join(source, 'USC-HAD')
usc = USCHAD('Uschad', uscFile, outPath, freq=100, trials_per_file=10000)
sig_usc = [SignalsUschad.acc_front_right_hip_X, SignalsUschad.acc_front_right_hip_Y,
           SignalsUschad.acc_front_right_hip_Z]
sig_usc += [SignalsUschad.gyr_front_right_hip_X, SignalsUschad.gyr_front_right_hip_Y,
            SignalsUschad.gyr_front_right_hip_Z]
usc.set_signals_use(sig_usc)
datasets.append(usc)

uciFile = os.path.join(source, 'uci-human-activity-recognition')
uci = UCIHAR('Ucihar', uciFile, outPath, freq=50, trials_per_file=10000)
sig_uci = [SignalsUcihar.acc_body_X, SignalsUcihar.acc_body_Y, SignalsUcihar.acc_body_Z]
sig_uci += [SignalsUcihar.gyr_body_X, SignalsUcihar.gyr_body_Y, SignalsUcihar.gyr_body_Z]
uci.set_signals_use(sig_uci)
datasets.append(uci)

preprocess_datasets(datasets)
# # Creating Loso evaluate generating in differents datafiles (no merging dataset)
selectedActs = ['Walking','Ascending stairs','Descending stairs','Standing','Sitting']
for dat in datasets:
	# preprocessing
	generate_ev = Loso([dat], overlapping=0.5, time_wd=2)
	# Save name of dataset in variable y
	generate_ev.set_name_act()
	generate_ev.set_act_processed()
	generate_ev.remove_action(selectedActivities = selectedActs)
	generate_ev.simple_generate(outPath, new_freq=25)
