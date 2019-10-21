#!/usr/bin/env python3
# encoding:utf8

"""
Task: Generate negative examples.
Author: Calvin,Xu
"""

import numpy as np
import random    
import sys

def getNegatives():
    """ Get train and test negatives. """
    positiveExamples = np.genfromtxt("positive_Examples", dtype=int, delimiter='\t', usecols=(0, 1))
    positiveExamples = set([tuple(row) for row in positiveExamples])

    trainUsersID = np.genfromtxt("train_UsersID", dtype=int)
    trainUsersID = set(trainUsersID)

    testUsersID = np.genfromtxt("test_UsersID", dtype=int)
    testUsersID = set(testUsersID)

    dtype = [("users_ID", int), ("locationID", "S80")]
    checkins = np.genfromtxt("train_Checkins", dtype=dtype, delimiter="\t", usecols=(0, 4))
    
    usersDict = dict()
    for e in checkins:
        if usersDict.get(e[1]) == None:
            usersDict[e[1]] = {e[0]}
        else:
            usersDict[e[1]].add(e[0])
    
    trainNegativeExamples = set()
    testNegativeExamples = set()
    for e in usersDict.values():
        co_location = sorted(list(e))
        i = 0
        for user01 in co_location:
            i += 1
            for user02 in co_location[i:]:
                if (user01, user02) not in positiveExamples:
                    if (user01 in trainUsersID) and (user02 in trainUsersID):
                        trainNegativeExamples.add((user01, user02, 0))
                    elif (user01 in testUsersID) and (user02 in testUsersID):
                        testNegativeExamples.add((user01, user02, 0))
                        

    np.savetxt("train_Negatives", np.array(list(trainNegativeExamples)), fmt="%s", delimiter='\t')
    np.savetxt("test_Negatives", np.array(list(testNegativeExamples)), fmt="%s", delimiter='\t')


if __name__ == '__main__':
    getNegatives()    # The parameter is train or test
