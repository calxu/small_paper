#!/usr/bin/env python3
# encoding:utf8

"""
Task: Learn model and make prediction.
Author: Calvin,Xu
"""

import numpy as np
import xgboost as xgb
import sys
import gc

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score           # The area of roc
from sklearn.metrics import average_precision_score # the area under the precision-recall curve
from sklearn.metrics import roc_curve


def readFeatures(filename):
    """ Read feature and label. """
    # user-pair in train data
    userPairsFeature = np.genfromtxt(filename, dtype=str, delimiter="\t")
    
    userFeature = []; label = []
    for e in userPairsFeature:
        allTimes = int(e[4])
        entropy  = float(e[5])
        userFeature.append([allTimes, entropy])
        label.append(int(e[2]))

    # initialize train user-pair feature and label
    data_X = np.array(userFeature)
    data_Y = np.array(label)

    # return train or test data matrix
    if ("train" in filename):
        # 4/5 data as train, and 1/5 data as evaluation
        length = len(data_Y) // 5 * 4            
        dtrain = xgb.DMatrix(data_X[:length], data_Y[:length])   # train data and label
        deval = xgb.DMatrix(data_X[length:], data_Y[length:])    # evaluation data and label
        return (dtrain, deval)
    elif ("test" in filename):
        dtest = xgb.DMatrix(data_X, data_Y)
        return dtest


def learnModel(dtrain, deval):
    """ Training model. """
    dtrainLabel = dtrain.get_label()
    # print("Negative numbers / Positive numbers = ", float(np.sum(dtrainLabel==0) / np.sum(dtrainLabel==1)))

    params = {'scale_pos_weight':float(np.sum(dtrainLabel == 0) / np.sum(dtrainLabel == 1)),
              'booster':'gbtree', 
              'max_depth':2, 
              'eta':0.1, 
              'silent':0, 
              'objective':'binary:logistic', 
              'eval_metric':'map'}
    watchlist = [(dtrain, 'Training'), (deval, 'Evaluation')]
    
    # training
    bst = xgb.train(params, dtrain, 100, watchlist, early_stopping_rounds=None)
    print("Weight: ", bst.get_score(importance_type='weight'))
    print("Gain:   ", bst.get_score(importance_type='gain'))
    print("Cover:  ", bst.get_score(importance_type='cover'))

    return bst 


def prediction(bst, dtest):
    """ Evaluate the social relationship strength. """
    # make prediction using trained model
    y_pred = bst.predict(dtest) 
    y_true = dtest.get_label()
    
    # assigned positive weight
    positiveWeight = np.sum(y_true == 0) / np.sum(y_true == 1)
    sample_weight = np.ones(dtest.num_row(), dtype=np.float)
    sample_weight[y_true == 1] = positiveWeight

    AUC = roc_auc_score(y_true, y_pred) 
    PR_AUC = average_precision_score(y_true, y_pred, sample_weight=sample_weight)
    print('AUC=', AUC, "PR-AUC=", PR_AUC, sep="\t") 
    
    # sort scores and corresponding truth values
    desc_score_indices = np.argsort(y_pred)[::-1]
    y_pred = y_pred[desc_score_indices]
    y_true = y_true[desc_score_indices]
    sample_weight = sample_weight[desc_score_indices]

    for topNumber in range(100, dtest.num_row(), 100):
        y_pred[:topNumber] = 1 
        y_pred[topNumber:] = 0

        precision = precision_score(y_true, y_pred, sample_weight=sample_weight)
        recall = recall_score(y_true, y_pred, sample_weight=sample_weight)
        # use command shell to redirect
        print("Top %d"%topNumber, "Precision: %f"%precision, "Recall: %f"%recall, sep="\t")  
    
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_pred, pos_label=1)
    fpr = fpr.reshape(-1, 1); tpr = tpr.reshape(-1, 1)
    np.savetxt(sys.argv[1]+"_auc_curve", np.hstack((fpr, tpr)), delimiter="\t")
    np.savetxt(sys.argv[1]+"_prediction", y_pred, fmt="%12.8f", delimiter="\t")
    """


def main(target):
    """ Train and test. """
    # Training
    dtrain, deval = readFeatures("./2_baseline_features/trainFeatures_" + target)
    bst = learnModel(dtrain, deval) 
    
    # recycle memory space
    del dtrain, deval; gc.collect()
    
    # Testing
    dtest = readFeatures("./2_baseline_features/testFeatures_" + target)
    prediction(bst, dtest)


if __name__ == '__main__':
    main(sys.argv[1])
