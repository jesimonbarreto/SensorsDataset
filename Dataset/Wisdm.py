from .Datasets import Dataset
from enum import Enum


class SignalsWisdm(Enum):
    acc_hand_X = 0
    acc_hand_Y = 1 
    acc_hand_Z = 2
class Wisdm(Dataset):

    def preprocess(self):
        file_name = self.dir_dataset
        output_dir = self.dir_save
        separator = '_'
        idx_label = 1

        f = open(file_name)
        lines = f.readlines()
        iterator = 0
        trial = []
        trial_id = 0
        for line in lines:
            try:
                split = line.strip().replace(';','').split(',')
                subject, act, time_stamp, x, y, z = split[0], split[1], split[2], split[3], split[4], split[5]
                #It is the same trial
                if iterator < len(lines)-1 and lines[iterator+1].split(',')[1] == act and lines[iterator+1].split(',')[0] == subject:
                    if time_stamp != '0': #timestamp equal to zero is a bug of the trial
                        v = []
                        data = []
                        for d in self.signals_use:
                            v.append(d.value)
                        if 0 in v:
                            data.append(float(x))
                        if 1 in v:
                            data.append(float(y))
                        if 2 in v:
                            data.append(float(z))
                        trial.append(data)

                #The next line will be a novel trial
                else:
                    print('{} {} {}'.format(act, subject, trial_id))
                    self.add_info_data(act, subject, trial_id, trial, output_dir)
                    #self.save_file(act, subject, trial_id, trial, self.dir_save)
                    trial_id = trial_id + 1
            except:
                print('Erro :'+line)
        self.save_data(output_dir)
