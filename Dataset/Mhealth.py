from Dataset.Datasets import Dataset
import glob


class MHEALTH(Dataset):

    def preprocess(self):
        files = glob.glob(pathname='*.log')
        output_dir = '../output'

        subject = 0
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            for line in lines:
                split = line.strip().split('        ')
                columns = len(split)-1
                if len(split) < 24:
                    print('Error')

                act = split[columns]

                #It is the same trial
                if iterator != len(lines)-1 and lines[iterator+1].split('   ')[len(split)-1].replace('\n','') == act:
                    trial.append(split[0:columns])

                #The next line will be a novel trial
                else:
                    self.save_file(act, subject, trial_id, trial)
                    trial_id = trial_id + 1
                    trial = []

                iterator = iterator + 1
            print('file_name:[{}] s:[{}]'.format(file, subject))