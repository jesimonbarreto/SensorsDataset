from .Datasets import Dataset
from enum import Enum
import numpy as np


class SignalsWisdm(Enum):
    acc_front_pants_pocket_X = 3
    acc_front_pants_pocket_Y = 4
    acc_front_pants_pocket_Z = 5


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

    def rename_act(self, act):
        return act.lower()

    def preprocess(self):
        filename = self.dir_dataset
        output_dir = self.dir_save

        output_dir = self.dir_save

        with open(filename, 'r') as f:
            fmt_data = {}
            instances = [line[:-1].split(',') for line in f.read().splitlines()]

            cur_subject = int(instances[0][0])
            cur_act = instances[0][1]
            trial = []
            for instance in instances:
                if len(instance) != 6:
                    continue

                instance[2:] = list(map(float, instance[2:]))

                subject = int(instance[0])
                act = instance[1]

                # Add keys to dict if they are not present
                if subject not in fmt_data:
                    fmt_data[subject] = {}
                if act not in fmt_data[subject]:
                    fmt_data[subject][act] = {}

                # Reset varaibles to add new trial on act change or subj change
                if cur_act != act or cur_subject != subject:
                    trial_id = max(list(fmt_data[subject][act].keys())) if len(list(fmt_data[subject][act].keys())) > 0 else 0
                    fmt_data[subject][act][trial_id + 1] = trial
                    cur_act = act
                    cur_subject = subject
                    trial = []
                
                trial.append(instance)

            for subject in fmt_data.keys():
                for act in fmt_data[subject].keys():
                    for trial_id, trial in fmt_data[subject][act].items():
                        trial = np.array(trial)

                        # Sort by timestamp
                        trial = trial[trial[:, 2].argsort()]

                        signals = [signal.value for signal in self.signals_use]
                        trial = trial[:, signals].astype(np.float)

                        # Filtro de NaNs
                        # indexes = np.sum(~np.isnan(trial), axis=1) == 54
                        # trial = trial[indexes]

                        self.add_info_data(act, subject, trial_id, trial, output_dir)
        self.save_data(output_dir)