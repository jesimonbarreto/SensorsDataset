from Dataset.Wisdm import Wisdm, SignalsWisdm as sw
from Dataset.Utdmhad1 import UTDMHAD1, SignalsUtdmhad1 as su1
from Dataset.Utdmhad2 import UTDMHAD2, SignalsUtdmhad2 as su2
from Dataset.Mhealth import MHEALTH, SignalsMHEALTH as sm
from Dataset.Wharf import WHARF, SignalsWharf as swh
from Dataset.Uschad import USCHAD, SignalsUSCHAD as susc
from Dataset.Pamap2 import PAMAP2, SignalsPAMAP2 as sp

from Process.Manager import preprocess_datasets
from Process.Protocol import Loso


if __name__ == "__main__":

    file_wisdm = 'Y:/sensors/originals/WISDM/WISDM_ar_v1.1_raw.txt'
    dir_datasets = 'C:/Users/sena/Desktop/Pesquisa/Codes/FrankDataset/2-residuals/results/dataset_preprocess/'
    dir_save_file = 'C:/Users/sena/Desktop/Pesquisa/Codes/FrankDataset/2-residuals/results/dataset_generated/'
    file_utd1 = 'Y:/sensors/originals/UTDMHAD/Inertial/'
    file_pm = 'Y:/sensors/originals/PAMAP2/Optional/'
    file_mh = 'Y:/sensors/originals/MHEALTHDATASET/'
    file_wharf = 'Y:/sensors/originals/WHARF'
    file_uschad = 'Y:/sensors/originals/USC-HAD'

    # Creating datasets
    # name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    wisdm = Wisdm('Wisdm', file_wisdm, dir_datasets, freq=20, trials_per_file=10000)
    wharf = WHARF('Wharf', file_wharf, dir_datasets, freq=32)
    utd1 = UTDMHAD2('UTD2', file_utd1, dir_datasets, freq=50)
    utd2 = UTDMHAD1('UTD1', file_utd1, dir_datasets, freq=50, trials_per_file=10000)
    p2 = PAMAP2('Pamap2', file_pm, dir_datasets, freq=50)
    mh = MHEALTH('Mhealth', file_mh, dir_datasets, freq=100)
    usc = USCHAD('USCHAD', file_uschad, dir_datasets, freq=100)

    # Define signals of each dataset
    sig_wisdm = [sw.acc_front_pants_pocket_X, sw.acc_front_pants_pocket_Y, sw.acc_front_pants_pocket_Z]
    wisdm.set_signals_use(sig_wisdm)

    sig_wharf = [swh.acc_right_wrist_X, swh.acc_right_wrist_Y, swh.acc_right_wrist_Z]
    wharf.set_signals_use(sig_wharf)

    sig_utd1 = [su1.acc_right_wrist_X, su1.acc_right_wrist_Y, su1.acc_right_wrist_Z]
    utd1.set_signals_use(sig_utd1)

    sig_utd2 = [su2.acc_right_thigh_X, su2.acc_right_thigh_Y, su2.acc_right_thigh_Z]
    utd2.set_signals_use(sig_utd2)

    sig_pm = [sp.acc1_dominant_wrist_X, sp.acc1_dominant_wrist_Y, sp.acc1_dominant_wrist_Z]
    p2.set_signals_use(sig_pm)

    sig_m = [sm.acc_right_lower_arm_X, sm.acc_right_lower_arm_Y, sm.acc_right_lower_arm_Z]
    mh.set_signals_use(sig_m)

    sig_usc = [susc.acc_front_right_hip_X, susc.acc_front_right_hip_Y, susc.acc_front_right_hip_Z]
    usc.set_signals_use(sig_usc)

    # list datasets
    datasets = [wisdm, utd2]

    # preprocessing
    preprocess_datasets(datasets)

    # Creating Loso evaluate generating
    generate_ev = Loso(datasets, overlapping=0.5, time_wd=5)
    # function to save information e data
    # files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq=20)



