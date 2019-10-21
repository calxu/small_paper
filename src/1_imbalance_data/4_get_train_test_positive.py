#!/usr/bin/env python
# encoding:utf8

"""
Task: Get train and test positive.
Author: Calvin,Xu.
"""

import numpy as np
import os

def getTrainTestPositives():
    """ Get train and test positive. """
    positiveExamples = np.genfromtxt("positive_Examples", dtype=int, delimiter='\t')
    trainUsersID = set(np.genfromtxt("train_UsersID", dtype=int))
    testUsersID  = set(np.genfromtxt("test_UsersID", dtype=int))

    trainPositives = []
    testPositives  = []
    
    for e in positiveExamples:
        if (e[0] in trainUsersID) and (e[1] in trainUsersID):
            trainPositives.append( [e[0], e[1], "1"] )
        elif ( e[0] in testUsersID ) and ( e[1] in testUsersID ):
            testPositives.append(  [e[0], e[1], "1"] )
    
    np.savetxt("train_Positives", trainPositives, fmt="%s", delimiter="\t")
    os.system("sort -n -k1,2 train_Positives > train_Positives.bak; \
               rm train_Positives; mv train_Positives.bak train_Positives")
    
    np.savetxt("test_Positives",  testPositives,  fmt="%s", delimiter="\t")
    os.system("sort -n -k1,2 test_Positives > test_Positives.bak; \
               rm test_Positives;  mv test_Positives.bak  test_Positives")


if __name__ == '__main__':
    getTrainTestPositives()
