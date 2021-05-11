from Dataset.Datasets import Dataset
import numpy as np
import glob

class PAMAP2(Dataset):

    def preprocess(self):
        files = glob.glob(pathname='Optional/*.dat')
        output_dir = '../output/2'
        idx_label = 1
        subject = 0
        #remove_columns = [0, 1, 2, 3,  16, 17, 18, 19, 20, 33, 34, 35, 36, 37, 50, 51, 52, 53]#Without temperature
        remove_columns = [0, 1, 2, 16, 17, 18, 19, 33, 34, 35, 36, 50, 51, 52, 53]#With temperature
        for file in files:
            f = open(file)
            lines = f.readlines()
            iterator = 0
            trial = []
            trial_id = 0
            subject = subject + 1
            incorrect = 0
            for line in lines:
                split = line.strip().split(' ')
                sample =  np.asarray(split)
                act = sample[1]

                sample = np.delete(sample, remove_columns)

                #It is the same trial
                #lines[iterator + 1].split(' ')[1] is the next activity
                if iterator != len(lines)-1 and lines[iterator+1].split(' ')[1] == act:
                    idx = np.where(sample == 'NaN')[0]
                    if(idx.size==0):
                        trial.append(sample)
                    else:#Incorrect file
                        incorrect = incorrect+1

                #The next line will be a novel trial
                else:
                    self.save_file(act, subject, trial_id, trial)
                    trial_id = trial_id + 1
                    trial = []


                iterator = iterator + 1
            print('file_name:[{}] s:[{}]'.format(file, subject))
            print('{} incorrect lines in file {}'.format(str(incorrect), file))
