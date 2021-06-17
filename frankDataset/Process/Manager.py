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