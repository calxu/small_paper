#!/usr/bin/env python3
# encoding:utf8

"""
Task: Get train and test usersID.
Author: Calvin,Xu.
"""

import numpy as np
import random
import sys

def getTrainTestUsers(trainingDataRatio=0.8):
    """ Get train and test usersID. """
    usersID = np.genfromtxt("users_ID", dtype=int, delimiter='\t')

    lengthTotalUsersID = len(usersID)
    lengthTrainUsersID = int(float(trainingDataRatio) * lengthTotalUsersID)
    totalUsersID = set(usersID)
    trainUsersID = set()
    
    while True:
        user_id = random.randint(0, lengthTotalUsersID-1)
        if usersID[user_id] not in trainUsersID:
            trainUsersID.add(usersID[user_id])

        if len(trainUsersID) == lengthTrainUsersID:
            break
    
    np.savetxt("train_UsersID", list(trainUsersID), fmt="%s", delimiter="\n")
    
    testUsersID = totalUsersID - trainUsersID
    np.savetxt("test_UsersID", list(testUsersID), fmt="%s", delimiter="\n")

if __name__ == '__main__':
    getTrainTestUsers(sys.argv[1])
