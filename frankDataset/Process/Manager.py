import numpy as np
import csv, sys, glob, os
import pandas as pd
from enum import Enum


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