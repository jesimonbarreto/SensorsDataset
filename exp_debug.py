from Dataset.Wisdm import Wisdm, SignalsWisdm as sw
from Dataset.Utdmhad1 import UTDMHAD1, SignalsUtdmhad1 as su1
from Dataset.Utdmhad2 import UTDMHAD2, SignalsUtdmhad2 as su2
from Dataset.Mhealth import MHEALTH, SignalsMHEALTH as sm
from Dataset.Wharf import WHARF, SignalsWharf as swh
from Dataset.Uschad import USCHAD, SignalsUSCHAD as susc
from Dataset.Pamap2 import PAMAP2, SignalsPAMAP2 as sp

from Process.Manager import preprocess_datasets
from Process.Protocol import Loso, MetaLearning
import os


if __name__ == "__main__":

    #dir_datasets = 'C:/Users/sena/Desktop/Pesquisa/Codes/FrankDataset/2-residuals/results/dataset_preprocess/'
    #dir_save_file = 'C:/Users/sena/Desktop/Pesquisa/Codes/FrankDataset/2-residuals/results/dataset_generated/'
    #file_utd1 = 'C:/Users/sena/Desktop/Pesquisa/Datasets/UTDMHAD'
    file_utd1 = '/storage/datasets/sensors/originals/UTDMHAD/'
    dir_datasets = '/mnt/users/jessica/Codes/frankdataset/2-residuals/results/dataset_preprocess/'
    dir_save_file = '/mnt/users/jessica/Codes/frankdataset/2-residuals/results/dataset_generated/'

    os.makedirs(dir_datasets, exist_ok=True)
    os.makedirs(dir_save_file, exist_ok=True)

    # Creating datasets
    # name, dir_dataset, dir_save, freq = 100, trial_per_file=100000
    utd2 = UTDMHAD2('UTD2', file_utd1, dir_datasets, freq=50, trials_per_file=10000)
    utd1 = UTDMHAD1('UTD1', file_utd1, dir_datasets, freq=50, trials_per_file=10000)

    # Define signals of each dataset
    sig_utd2 = [su2.acc_right_thigh_X, su2.acc_right_thigh_Y, su2.acc_right_thigh_Z]
    utd2.set_signals_use(sig_utd2)

    sig_utd1 = [su1.acc_right_wrist_X, su1.acc_right_wrist_Y, su1.acc_right_wrist_Z]
    utd1.set_signals_use(sig_utd1)

    # list datasets
    datasets = [utd2]

    # preprocessing
    preprocess_datasets(datasets)

    train_labels = ['UTD2-jogging', 'UTD2-walking', 'UTD2-sit to stand']
    test_labels = ['UTD2-squat']

    # Creating Loso evaluate generating
    generate_ev = MetaLearning(datasets, train_labels, test_labels, overlapping=0.0, time_wd=1)
    generate_ev.set_name_act()
    # function to save information e data
    # files = glob.glob(dir_datasets+'*.pkl')
    generate_ev.simple_generate(dir_save_file, new_freq=20)



