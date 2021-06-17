from .Datasets import Dataset
from enum import Enum
import numpy as np


class SignalsWisdm(Enum):
    acc_front_pants_pocket_X = 0
    acc_front_pants_pocket_Y = 1
    acc_front_pants_pocket_Z = 2


actNameWISDM = {
    1: 'Walking',
    2: 'Jogging',
    3: 'Upstairs',
    4: 'Downstairs',
    5: 'Sitting',
    6: 'Standing'
}


class Wisdm(Dataset):

    def print_info(self):
        return """
                device: cellphone
                frequency: 20Hz
                positions: front pants leg pocket
                sensors: acc
                """

    def preprocess(self):
        file_name = self.dir_dataset
        output_dir = self.dir_save

        f = open(file_name)
        lines = f.readlines()
        trial = []
        trial_id = 0
        for current_line, line in enumerate(lines):
            try:
                # if current line is \n
                if len(line.strip().replace(';','').split(',')) < 2:
                    print('Erro :' + line)
                    continue
                else:
                    split = line.strip().replace(';','').split(',')
                    subject, act, time_stamp, x, y, z = split[0], split[1], split[2], split[3], split[4], split[5]
                    sample = self.get_sample(x, y, z)

                    # if next line is \n
                    if len(lines[current_line+1].split(',')) < 2:
                        # timestamp equal to zero is a bug of the trial
                        if time_stamp != '0':
                            trial.append(sample)

                    # It is the same trial and is not the last line of this current trial
                    elif current_line < len(lines)-1 and lines[current_line+1].split(',')[1] == act and lines[current_line+1].split(',')[0] == subject:
                        # timestamp equal to zero is a bug of the trial
                        if time_stamp != '0':
                            trial.append(sample)

                    # The next line will be a novel trial
                    else:
                        # add the current line
                        # timestamp equal to zero is a bug of the trial
                        if time_stamp != '0':
                            trial.append(sample)
                        # convert to numpy
                        trial_np = np.array(trial)
                        # save the trial
                        self.add_info_data(act, subject, trial_id, trial_np, output_dir)
                        # initiate a new trial
                        trial = []
                        trial_id = trial_id + 1

            except:
                print('[Except] Erro :' + line)
        self.save_data(output_dir)

    def get_sample(self, x, y, z):
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
        return data
