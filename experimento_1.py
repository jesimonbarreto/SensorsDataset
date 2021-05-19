from Dataset.Wisdm import Wisdm, SignalsWisdm as sw
from Dataset.Mhealth import MHEALTH, SignalsMHEALTH as sm
from Dataset.Wharf import WHARF, SignalsWharf as swh
from Dataset.Uschad import USCHAD, SignalsUSCHAD as susc
from Dataset.Pamap2 import PAMAP2, SignalsPAMAP2 as sp

from Process.Manager import preprocess_datasets
from Process.Protocol import MetaLearning
import os


if __name__ == "__main__":

    file_wisdm = '/storage/datasets/sensors/originals/WISDM/WISDM_ar_v1.1_raw.txt'
    dir_datasets = '/mnt/users/jessica/Codes/frankdataset/2-residuals/results/dataset_preprocess/'
    dir_save_file = '/mnt/users/jessica/Codes/frankdataset/2-residuals/results/dataset_generated/'
    file_pm = '/storage/datasets/sensors/originals/PAMAP2/Optional/'
    file_mh = '/storage/datasets/sensors/originals/MHEALTHDATASET/'
    file_wharf = '/storage/datasets/sensors/originals/WHARF'
    file_uschad = '/storage/datasets/sensors/originals/USC-HAD'

    os.makedirs(dir_datasets, exist_ok=True)
    os.makedirs(dir_save_file, exist_ok=True)

    # Creating datasets
    # name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    wisdm = Wisdm('wisdm', file_wisdm, dir_datasets, freq=20, trials_per_file=100000)
    wharf = WHARF('wharf', file_wharf, dir_datasets, freq=32, trials_per_file=100000)
    p2 = PAMAP2('pamap2', file_pm, dir_datasets, freq=50, trials_per_file=100000)
    mh = MHEALTH('mhealth', file_mh, dir_datasets, freq=100, trials_per_file=100000)
    usc = USCHAD('uschad', file_uschad, dir_datasets, freq=100, trials_per_file=100000)

    # Define signals of each dataset
    sig_wisdm = [sw.acc_front_pants_pocket_X, sw.acc_front_pants_pocket_Y, sw.acc_front_pants_pocket_Z]
    wisdm.set_signals_use(sig_wisdm)

    sig_wharf = [swh.acc_right_wrist_X, swh.acc_right_wrist_Y, swh.acc_right_wrist_Z]
    wharf.set_signals_use(sig_wharf)

    sig_pm = [sp.acc1_dominant_wrist_X, sp.acc1_dominant_wrist_Y, sp.acc1_dominant_wrist_Z]
    p2.set_signals_use(sig_pm)

    sig_m = [sm.acc_right_lower_arm_X, sm.acc_right_lower_arm_Y, sm.acc_right_lower_arm_Z]
    mh.set_signals_use(sig_m)

    sig_usc = [susc.acc_front_right_hip_X, susc.acc_front_right_hip_Y, susc.acc_front_right_hip_Z]
    usc.set_signals_use(sig_usc)

    # list datasets
    datasets = [wisdm, wharf, p2, mh, usc]

    # preprocessing
    preprocess_datasets(datasets)

    train_labels = ['UTD2-jogging', 'UTD2-walking', 'UTD2-sit to stand']
    test_labels = ['UTD2-squat']

    # Creating Loso evaluate generating
    generate_ev = MetaLearning(datasets, train_labels, test_labels, overlapping=0.5, time_wd=5)
    generate_ev.set_name_act()
    # function to save information e data
    # files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq=20)



