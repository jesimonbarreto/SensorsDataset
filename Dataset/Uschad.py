from Dataset.Datasets import Dataset
from scipy.io import loadmat


class USCHAD(Dataset):
    def preprocess(self):
        mat_files = []
        for root, dirs, files in os.walk(self.dir_dataset):
            if len(dirs) == 0:
                mat_files = [os.path.join(root, f) for f in files]

        for filepath in mat_files:
            mat_file = loadmat(filepath)
            act = mat_file['activity'][0]
            subject = int(mat_file['subject'][0])
            trial_id = int(mat_file['trial'][0])
            trial = mat_file['sensor_readings']

            self.add_info_data(act, subject, trial_id, trial, self.dir_save)
            print('file_name:[{}] s:[{}]'.format(filepath, subject))

        self.save_data(self.dir_save)