from .Datasets import Dataset
class cook2020(Dataset):
	#https://abc-research.github.io/cook2020/
	
	def preprocess(self, sensor_list =  ['left_hip' ,'left_wrist' ,'right_arm' ,'right_wrist']):
		def parse_IMU(parent_dir, sub_dirs, startTime, endTime, file_name, window_length):
			data = []
			data_count = 0
			for sub_dir in sub_dirs:
				channel = []
				for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_name)):
					file = open(fn, newline='')
					reader = csv.reader(file)
					first = True
					count = 0
					for row in reader:
						if first:
							first = False
							continue
						try:
							timestamp = float(row[3])  # 4th column is timestamp
						except:
							row = row[0].split(';')
							timestamp = float(row[3])
						window_jitter1 = random.randint(-150, 150)
						window_jitter2 = random.randint(-150, 150)
						if timestamp >= (startTime + window_jitter1) and timestamp <= (
								endTime + window_jitter2) and count < window_length:
							
							try:
								channel.append([float(row[0]), float(row[1]), float(row[2])])
							except:
								continue
							count = count + 1
							data_count = data_count + 1
				data.append(channel)
			return data, data_count
		# merge train and test first!
		
		min_data_count = 100
		sub_dirs = sensor_list
		files = os.listdir(os.path.join(self.dir_dataset, sub_dirs[0]))
		number_of_samples = 500
		
		trial_id_ = dict()
		trial_id_['1'] = 0
		trial_id_['2'] = 0
		trial_id_['3'] = 0
		trial_id_['4'] = 0
		
		
		# read the labels
		labels_loc = os.path.join(self.dir_dataset, 'LabelTable.csv')
		file_label = open(labels_loc, newline='', encoding="utf8")
		label_reader = pd.read_csv(labels_loc, sep=';', index_col=0, header=[0, 1]).iloc[:, 0:1]
		
		for f in files:
			st_index = 0
			end_index = 30000
			step = 1000  # overlapping window, step
			window_index = 10000  # 6 second window
			f_name = f.split('.')[0]
			
			if f_name not in pd.unique(label_reader.index):
				continue
			
			curr_label_file = label_reader.loc[f_name].values[0]
			curr_subject = f_name.split('_')[0][-1]
			while st_index + step < end_index:
				
				data, data_count = parse_IMU(self.dir_dataset, sub_dirs, st_index, st_index + window_index, f,
				                             number_of_samples)
				st_index = st_index + step
				
				if data_count < min_data_count:
					continue
				
				
				train_data_sample = np.zeros((len(sensor_list ) *3, number_of_samples))
				train_data_label = curr_label_file
				for i in range(len(data)):
					for j in range(len(data[i])):
						train_data_sample[i * 3, j] = data[i][j][0]
						train_data_sample[i * 3 + 1, j] = data[i][j][1]
						train_data_sample[i * 3 + 2, j] = data[i][j][2]
				trial = np.transpose(train_data_sample, (1, 0))
				# trial = np.expand_dims(act, axis=0)
				act = train_data_label[0].upper() + train_data_label[1:]
				trial_id = trial_id_[curr_subject]
				trial = train_data_sample
				self.add_info_data(act, curr_subject ,trial_id , trial, self.dir_save)
				trial_id_[curr_subject] += 1
		self.save_data(self.dir_save)
