import shutil

from Dataset.Wisdm import Wisdm, SignalsWisdm as sw
from Dataset.Mhealth import MHEALTH, SignalsMHEALTH as sm
from Dataset.Wharf import WHARF, SignalsWharf as swh
from Dataset.Uschad import USCHAD, SignalsUSCHAD as susc
from Dataset.Pamap2 import PAMAP2, SignalsPAMAP2 as sp

from Process.Manager import preprocess_datasets
from Process.Protocol import MetaLearningICU
import os

from Utils.utils_metalearning import target_task_health
from tqdm import tqdm
import time
import argparse
import numpy as np


def instanciate_dataset(datasets_list, dir_datasets):
    file_wisdm = 'X:/sensors/originals/WISDM/WISDM_ar_v1.1_raw.txt'
    file_pm = 'X:/sensors/originals/PAMAP2/'
    file_mh = 'X:/sensors/originals/MHEALTHDATASET/'
    file_wharf = 'X:/sensors/originals/WHARF/WHARF Data Set/Data/'
    file_uschad = 'X:/sensors/originals/USC-HAD'

    datasets = []
    # Creating datasets
    # name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    wisdm = Wisdm('wisdm', file_wisdm, dir_datasets, freq=20, trials_per_file=100000)
    if 'wisdm' in datasets_list:
        datasets.append(wisdm)
        sig_wisdm = [sw.acc_front_pants_pocket_X, sw.acc_front_pants_pocket_Y, sw.acc_front_pants_pocket_Z]
        wisdm.set_signals_use(sig_wisdm)

    wharf = WHARF('wharf', file_wharf, dir_datasets, freq=32, trials_per_file=100000)
    if 'wharf' in datasets_list:
        datasets.append(wharf)
        sig_wharf = [swh.acc_right_wrist_X, swh.acc_right_wrist_Y, swh.acc_right_wrist_Z]
        wharf.set_signals_use(sig_wharf)

    p2 = PAMAP2('pamap2', file_pm, dir_datasets, freq=100, trials_per_file=100000)
    if 'pamap2' in datasets_list:
        datasets.append(p2)
        sig_pm = [sp.acc1_dominant_wrist_X, sp.acc1_dominant_wrist_Y, sp.acc1_dominant_wrist_Z]
        p2.set_signals_use(sig_pm)

    mh = MHEALTH('mhealth', file_mh, dir_datasets, freq=50, trials_per_file=100000)
    if 'mhealth' in datasets_list:
        datasets.append(mh)
        sig_m = [sm.acc_right_lower_arm_X, sm.acc_right_lower_arm_Y, sm.acc_right_lower_arm_Z]
        mh.set_signals_use(sig_m)

    usc = USCHAD('uschad', file_uschad, dir_datasets, freq=100, trials_per_file=100000)
    if 'uschad' in datasets_list:
        datasets.append(usc)
        sig_usc = [susc.acc_front_right_hip_X, susc.acc_front_right_hip_Y, susc.acc_front_right_hip_Z]
        usc.set_signals_use(sig_usc)

    return datasets


def process_datasets(datasets):
    # preprocessing
    print("\nDatasets preprocessing...\n", flush=True)
    preprocess_datasets(datasets)
    print("\nDone.\n", flush=True)

    return datasets


def create_dataset(datasets, dir_save_file, dir_datasets, source_tasks, target_tasks, exp_name,
                   overlapping, time_wd, new_freq):
    # Creating Loso evaluate generating
    generate_ev = MetaLearningICU(datasets, dir_datasets, source_tasks, target_tasks, exp_name, overlapping=overlapping,
                               time_wd=time_wd)
    generate_ev.set_name_act()
    # function to save information e data
    # files = glob.glob(dir_datasets+'*.pkl')
    print("\n--Npz generating--\n", flush=True)
    generate_ev.simple_generate(dir_save_file, new_freq=new_freq)

    print("\nNpz Done.\n", flush=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        import pydevd_pycharm

        pydevd_pycharm.settrace('172.22.100.3', port=9000, stdoutToServer=True, stderrToServer=True, suspend=False)

    dir_datasets = 'C:/Users/jsena/Documents/Pesquisa/Codes/DA-healthy2patient/2-residuals/dataset_preprocess/'
    dir_save_file = 'C:/Users/jsena/Documents/Pesquisa/Codes/DA-healthy2patient/2-residuals/'

    overlapping = 0.5
    time_wd = 5
    new_freq = 20

    if not os.path.exists(dir_datasets):
        os.makedirs(dir_datasets)
    if not os.path.exists(dir_save_file):
        os.makedirs(dir_save_file)

    #datasets_list = ['mhealth', 'wharf', 'wisdm', 'uschad', 'pamap2']
    # debug porpouses
    datasets_list = ['uschad', 'pamap2']

    datasets = instanciate_dataset(datasets_list, dir_datasets)

    #process_datasets(datasets)
    target_dataset = datasets_list[0]
    source_dataset = datasets_list[1]
    print("Target dataset: {}".format(target_dataset), flush=True)
    start = time.time()
    target_tasks = target_task_health(target_dataset)

    source_tasks = target_task_health(source_dataset)
    source_names = "_{}".format(source_dataset)
    exp_name = "3ways_target[{}]_source[{}]_metalearning_ICU".format(target_dataset, source_names)
    create_dataset(datasets, dir_save_file, dir_datasets, source_tasks, target_tasks, exp_name,
                   overlapping, time_wd, new_freq)
    end = time.time()
    print("Time passed target dataset {} = {}".format(target_dataset, end - start), flush=True)
