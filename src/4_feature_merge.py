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


def readBaselineFeatures(filename):
    """ Read feature and label. """
    # user-pair in train data
    userPairsFeature = np.genfromtxt(filename, dtype=str, delimiter="\t")
    
    userFeature = []
    for e in userPairsFeature:
        allTimes = [int(e[4]), int(e[6]), int(e[8]), int(e[10])]
        entropy  = [float(e[5]), float(e[7]), float(e[9]), float(e[11])]
        userFeature.append([*allTimes, *entropy])

    return userFeature


def readOtherFeatures(filename):
    """ Read the other co-occurrence features, e.g. topic co-occurrence and context co-occurrence. """
    userIdFeature = np.genfromtxt(filename, dtype=np.float, delimiter="\t")

    userFeature = dict()
    for e in userIdFeature:
        userid = int(e[0])
        userFeature[userid] = list(e[1:])
    
    return userFeature


def featureMerge(filename, baseline, topic_cooccurrence, context_cooccurrence):
    """ Feature merge. """
    userPairs = np.genfromtxt(filename, dtype=np.int, delimiter="\t")
    
    data_X = []; data_Y = []
    for e in zip(userPairs, baseline):
        userFeatures = [ *e[1], *topic_cooccurrence[0][e[0][0]], *topic_cooccurrence[0][e[0][1]], *topic_cooccurrence[1][e[0][0]],\
           *topic_cooccurrence[1][e[0][1]], *context_cooccurrence[0][e[0][0]], *context_cooccurrence[0][e[0][1]],\
           *context_cooccurrence[1][e[0][0]], *context_cooccurrence[1][e[0][1]] ]

        data_X.append(userFeatures)
        data_Y.append(e[0][2])

    # initialize train user-pair feature and label
    data_X = np.array(data_X)
    data_Y = np.array(data_Y)

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
              'eval_metric':'auc'}
    watchlist = [(dtrain, 'Training'), (deval, 'Evaluation')]
    
    # training
    bst = xgb.train(params, dtrain, 300, watchlist, early_stopping_rounds=10)
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

    for topNumber in range(500, dtest.num_row(), 500):
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


def main():
    """ Train and test. """
    # feature merge
    topic_day = readOtherFeatures("./2_topic_features/topic_features/feature_day")
    topic_location = readOtherFeatures("./2_topic_features/topic_features/feature_location")
    context_cooccurrence_day = readOtherFeatures("./2_context_cooccurrence/Feature/feature_day")
    context_cooccurrence_location = readOtherFeatures("./2_context_cooccurrence/Feature/feature_location")

    trainBaseline = readBaselineFeatures("./2_baseline_features/trainFeatures_merge")
    testBaseline = readBaselineFeatures("./2_baseline_features/testFeatures_merge")

    # Training
    dtrain, deval = featureMerge("./1_imbalance_data/train_Data", trainBaseline, (topic_day, topic_location), \
                                 (context_cooccurrence_day, context_cooccurrence_location))

    bst = learnModel(dtrain, deval)

    # recycle memory sapce
    del dtrain, deval; gc.collect()
    
    # Testing
    dtest = featureMerge("./1_imbalance_data/test_Data", testBaseline, (topic_day, topic_location), \
                                 (context_cooccurrence_day, context_cooccurrence_location))

    prediction(bst, dtest)


if __name__ == '__main__':
    main()
