import shutil

from Dataset.Wisdm import Wisdm, SignalsWisdm as sw
from Dataset.Mhealth import MHEALTH, SignalsMHEALTH as sm
from Dataset.Wharf import WHARF, SignalsWharf as swh
from Dataset.Uschad import USCHAD, SignalsUSCHAD as susc
from Dataset.Pamap2 import PAMAP2, SignalsPAMAP2 as sp

from Process.Manager import preprocess_datasets
from Process.Protocol import MetaLearning
import os

from Utils.utils_metalearning import all_activities, target_task_top4, all_activities_all_datasets
from tqdm import tqdm
import time
import argparse
import numpy as np


def instanciate_dataset(datasets_list, dir_datasets):

    file_wisdm = '/storage/datasets/sensors/originals/WISDM/WISDM_ar_v1.1_raw.txt'
    file_pm = '/storage/datasets/sensors/originals/PAMAP2/'
    file_mh = '/storage/datasets/sensors/originals/MHEALTHDATASET/'
    file_wharf = '/storage/datasets/sensors/originals/WHARF/WHARF Data Set/Data/'
    file_uschad = '/storage/datasets/sensors/originals/USC-HAD'

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


def create_dataset(datasets, datasets_list, dir_save_file, dir_datasets, source_tasks, target_tasks, exp_name,
                   overlapping, time_wd, new_freq):
    # Creating Loso evaluate generating
    generate_ev = MetaLearning(datasets, dir_datasets, source_tasks, target_tasks, exp_name, overlapping=overlapping,
                               time_wd=time_wd)
    generate_ev.set_name_act()
    # function to save information e data
    # files = glob.glob(dir_datasets+'*.pkl')
    print("\n--Npz generating--\n", flush=True)
    X_train, y_train, X_val, y_val, X_test, y_test = generate_ev.simple_generate(dir_save_file, new_freq=new_freq)

    all_act = all_activities_all_datasets(datasets_list)

    final_act = list(np.unique(y_train))
    final_act.extend(list(np.unique(y_val)))
    final_act.extend(list(np.unique(y_test)))
    final_act = np.unique(final_act)
    diff = set(all_act).difference(set(final_act))

    if len(diff):
        print("\n\nActivities not used to make this dataset: {}\n".format(len(diff)))
        print(diff)
    else:
        print("\n\nAll activities were used in this dataset:\n")

    print("\nNpz Done.\n", flush=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        import pydevd_pycharm

        pydevd_pycharm.settrace('172.22.100.3', port=9000, stdoutToServer=True, stderrToServer=True, suspend=False)

    dir_datasets = '/mnt/users/jessica/Codes/frankdataset/2-residuals/results/dataset_preprocess/'
    dir_save_file = '/storage/datasets/sensors/nshot_experiments/pra_rodar/'

    overlapping = 0
    time_wd = 5
    new_freq = 20

    if not os.path.exists(dir_datasets):
        os.makedirs(dir_datasets)
    if not os.path.exists(dir_save_file):
        os.makedirs(dir_save_file)

    datasets_list = ['mhealth', 'wharf', 'wisdm', 'uschad', 'pamap2']
    # debug porpouses
    #datasets_list = ['pamap2']

    datasets = instanciate_dataset(datasets_list, dir_datasets)

    process_datasets(datasets)
    
    for target_dataset in tqdm(datasets_list):
        print("Target dataset: {}".format(target_dataset), flush=True)
        exp_name = "1_" + target_dataset
        start = time.time()
        target_tasks = target_task_top4(target_dataset)

        source_dataset = [d for d in datasets_list if d not in target_dataset]
        source_tasks = []
        source_names = ''
        for dt in source_dataset:
            source_tasks.extend(all_activities(dt))
            source_names += "_{}".format(dt)
        exp_name = "4ways_target[{}]_source[{}]_exp1_d".format(target_dataset, source_names)
        create_dataset(datasets, datasets_list, dir_save_file, dir_datasets, source_tasks, target_tasks, exp_name,
                       overlapping, time_wd, new_freq)
        end = time.time()
        print("Time passed target dataset {} = {}".format(target_dataset, end-start), flush=True)
