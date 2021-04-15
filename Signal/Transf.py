import numpy as np                  # for working with tensors outside the network
import pandas as pd                 # for data reading and writing
import matplotlib.pyplot as plt     # for data inspection
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
import math
import pickle
from sklearn.metrics.classification import accuracy_score, recall_score, f1_score
import scipy.stats as st
import sys
import custom_model as cm
import cv2, json
import matplotlib.image as mpimg
from scipy.interpolate import interp1d
from fastpip import pip



def sampling_rate(data, rate_reduc):
    number_samp = int(data[0].shape[-2])
    samples_slct = list(range(0,number_samp,rate_reduc))
    new_data = [data[0][:,:,samples_slct,:]]
    return new_data

def interpo(data, tp, n_samples):
    samples = data[0]
    shape = samples.shape
    new_samples = []
    for smp in samples:
        smp = smp[0]
        s = []
        for sig in range(3):
            size = int(smp.shape[0])
            x = np.linspace(0, size-1, num=size, endpoint=True)
            y = smp[:,sig]
            f = interp1d(x, y, kind= tp)
            x_new = np.linspace(0, size-1, num=n_samples, endpoint=True)
            y_new = f(x_new)
            s.append(y_new)
        s = np.array(s)
        new_samples.append(s)
    new_samples = np.array(new_samples)
    new_samples = new_samples.reshape(shape[0],shape[1],n_samples,shape[3])
    return [new_samples]

def pip_sample(data, n_samples):
    number_samp = int(data[0].shape[-2])
    number_s = int(data[0].shape[0])
    final = []
    for samp in data[0]:
        samp = samp[0]
        x_pip = []
        y_pip = []
        z_pip = []
        for j in range(number_samp):
            x_pip.append((j,samp[:,0][j]))
            y_pip.append((j,samp[:,1][j]))
            z_pip.append((j,samp[:,2][j]))
        x_pip = pip(x_pip,n_samples)
        y_pip = pip(y_pip,n_samples)
        z_pip = pip(z_pip,n_samples)
        x_pip = np.array(list(zip(*x_pip))[1]).reshape(-1,1)
        y_pip = np.array(list(zip(*y_pip))[1]).reshape(-1,1)
        z_pip = np.array(list(zip(*z_pip))[1]).reshape(-1,1)
        final.append(np.concatenate((x_pip,y_pip,z_pip),axis=1))

    data_final = [np.array(final).reshape(number_s,1,n_samples,3)]
    return data_final


def select_features(X, y, d_act):
    y = np.argmax(y, axis=1)
    X_new = []
    y_new = []
    for idx,act in enumerate(d_act):
        ind = np.where(y==act)
        if idx == 0:
            X_new = X[ind]
            y_new = np.array([idx]*len(ind[0]))
        else:
            X_new = np.concatenate((X_new,X[ind]),axis=0)
            y_new = np.concatenate((y_new,np.array([idx]*len(ind[0]))),axis=0)

    y_new = to_categorical(y_new)
    return X_new, y_new

PATH = '/home/jesimonsantos/datasets/sensor_RP/'
d1_activity = [3,10,1,0,4,2] #Mhealth, walk, run, sit, stand,clib. stairs, layins
d2_activity = [7,10,1,2,5,0] #PAMA


if __name__ == '__main__':
    np.random.seed(12227)

    batch = 100
    samp_rate_1 = 0
    samp_rate_2 = 0
    tp = 'linear'
    amp_rate_1 = 200
    amp_rate_2 = 0
    data_input_file = '/home/jesimon/home_qnap/sensor/datasets/LOSO/UTD-MHAD2_1s.npz'
    data_input_file_2 = '/home/jesimon/home_qnap/sensor/datasets/LOSO/UTD-MHAD2_1s.npz'

    if len(sys.argv) > 2:
        data_input_file = sys.argv[1]
        data_input_file_2 = sys.argv[2]
        samp_rate_1 = int(sys.argv[3])
        samp_rate_2 = int(sys.argv[4])


    print('Dataset 1 - {};\nDataset 2 - {}\n'.format(data_input_file, data_input_file_2))
    print('info: Type amp {}'.format(tp))
    print('Dataset 1 -- Reduc rate {}; Amp. points {}'.format(samp_rate_1, amp_rate_1))
    print('Dataset 2 -- Reduc rate {}; Amp. points {}\n\n'.format(samp_rate_2, amp_rate_2))
    tmp = np.load(data_input_file, allow_pickle=True)
    sys.stdout.flush()

    X = tmp['X']
    y = tmp['y']
    folds = tmp['folds']
    dataset_name = data_input_file.split('/')[-1]
    print('Loaded {} with success'.format(dataset_name))

    X, y = select_features(X, y, d1_activity)

     n_classes = y.shape[1]
    #y = np.argmax(y, axis=1)

    print(data[0].shape)

    if amp_rate_1 != 0:
        #data = interpo(data, tp, amp_rate_1)
        data = pip_sample(data, amp_rate_1)

    print(data[0].shape)

    if samp_rate_1 != 0:
        data = sampling_rate(data, samp_rate_1)

    print(data[0].shape)

    avg_acc = []
    avg_recall = []
    avg_f1 = []

