import numpy as np
import keras
from sklearn.metrics.classification import accuracy_score, recall_score, f1_score
import scipy.stats as st
import sys
import custom_model as cm

from keras import backend as K
from keras.models import load_model
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



if __name__ == '__main__':
    np.random.seed(12227)
    
    
    if len(sys.argv) > 1:
        data_input_file = sys.argv[1]
    else:
        data_input_file = '/mnt/users/jessica/datasets/LOSO/MHEALTH.npz'
        #data_input_file = 'Z:/datasets/LOSO/MHEALTH.npz'

    tmp = np.load(data_input_file, allow_pickle=True)
    X = tmp['X']
    # For sklearn methods X = X[:, 0, :, :]
    y = tmp['y']
    folds = tmp['folds']
    n_class = y.shape[1]


    model = load_model('Sena2018_model_' + dataset_name.split(".")[0] + '_fold0.h5')

    feature_layer = K.function([model.layers[0].input, model.layers[1].input, model.layers[2].input, K.learning_phase()], [model.layers[168].output])

    features = feature_layer([X_train[0], X_train[1], X_train[2], 0])[0]
    # features = []
    # for v in X_features:
    #     features.append(v.flatten())
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(features)
    y_one = [np.argmax(x) for x in y[train_idx]]
    # lda = LDA(n_components=2)
    # principalComponents = lda.fit_transform(features, y_one)
    # principalComponents = lda.transform(features)
    # lda = LDA(n_components=2)
    # principalComponents = lda.fit(features, y_one).transform(features)
    principalDf = pd.DataFrame(data=principalComponents
                               , columns=['First Component', 'Second Component'])

    y_pd = pd.DataFrame(data=y_one, columns=['target'])

    finalDf = pd.concat([principalDf, y_pd], axis=1)


    ######### 2D ##############

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('First Component', fontsize=15)
    ax.set_ylabel('Second Component', fontsize=15)
    ax.set_title('MHEALTH Activities Features', fontsize=20)
    cmap = get_cmap(n_class)
    targets = []
    colors = []
    for i in range(n_class):
        targets.append(i)
        colors.append(cmap(i))
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'First Component']
                   , finalDf.loc[indicesToKeep, 'Second Component']
                   , c=color
                   , s=50)
    ax.legend(targets)
    ax.grid()
    #plt.show()
    plt.savefig('Sena2018_model_layer168' + dataset_name.split(".")[0] + '_fold0.png')
    plt.clf()

    ######### 3D ##############
    # features = []
    # for v in X_train[0]:
    #     features.append(v.flatten())
    #
    # pca = PCA(n_components=3)
    # principalComponents = pca.fit_transform(features)
    # lda = LDA(n_components=3)
    # principalComponents = lda.fit_transform(features, y_one)
    # principalDf = pd.DataFrame(data=principalComponents, columns=['First Component', 'Second Component', 'Third Component'])
    #
    # y_pd = pd.DataFrame(data=y_one, columns=['target'])
    #
    # finalDf = pd.concat([principalDf, y_pd], axis=1)
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # cmap = get_cmap(n_class)
    # targets = []
    # colors = []
    # for i in range(n_class):
    #     targets.append(i)
    #     colors.append(cmap(i))
    # for target, color in zip(targets, colors):
    #     indicesToKeep = finalDf['target'] == target
    #     ax.scatter(finalDf.loc[indicesToKeep, 'First Component']
    #                , finalDf.loc[indicesToKeep, 'Second Component'],  finalDf.loc[indicesToKeep, 'Third Component']
    #                , c=color
    #                , s=50)
    # ax.legend(targets)
    # ax.grid()
    # plt.savefig('Sena2018_model_layer168' + dataset_name.split(".")[0] + '_fold0_3D.png')
    # plt.clf()
    # plt.show()



    # output in train mode = 1
    #layer_output = get_3rd_layer_output([x, 1])[0]

   # Your testing goes here. For instance:
   # y_pred = _model.predict(X_test)
