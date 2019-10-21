#!/usr/bin/env python3
# encoding:utf8

"""
Task: Generate negative example.
Author: Calvin,Xu
"""

import numpy as np
import random    
import sys

def getNegatives(target):
    """ Get train and test negative. """
    positiveExamples = np.genfromtxt(target + "_Positives", dtype=int, delimiter='\t', usecols=(0, 1))
    usersID = np.genfromtxt(target + "_UsersID", dtype=int, delimiter='\t')

    lengthUsersID = len(usersID)
    positiveExamples = set([tuple(row) for row in positiveExamples])
    negativeExamples = set()

    while True:                                             # generate random user relationship and label 0 on the data
        user_1 = random.randint(0, lengthUsersID-1)         # range [0, len(length of vocabulary)]
        user_2 = random.randint(0, lengthUsersID-1)

        if user_1 == user_2:                                # ensure two different user
            continue                                

        userId = [user_1, user_2] if(user_1 < user_2) else [user_2, user_1]    # [smaller user id, larger user id]
        relationship = ( usersID[userId[0]], usersID[userId[1]], 0 )
        
        if ((relationship[0], relationship[1]) in positiveExamples) or (relationship in negativeExamples):
            continue

        negativeExamples.add(relationship)

        if len(negativeExamples) == len(positiveExamples):    # keep data balance (the number of positive_example == the number of negative_example)
            break
    
    np.savetxt(target + "_Negatives", np.array(list(negativeExamples)), fmt="%s", delimiter='\t')

if __name__ == '__main__':
    getNegatives(sys.argv[1])    # The parameter is train or test
