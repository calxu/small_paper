#!/usr/bin/env python
# encoding:utf8

"""
Task: Generate positive example.
Author: Calvin,Xu.
"""

import numpy as np
import os

def getPositive():
    """ Get Positive Example. """
    filename = os.popen("ls ../ | grep 'edges.txt'").read().strip()
    positiveExamples = np.genfromtxt("../" + filename, dtype=int, delimiter='\t')
    usersID = np.genfromtxt("users_ID", dtype=int, delimiter='\t')
    
    usersID = set(usersID)
    for e in positiveExamples:
        if e[0] > e[1]:                                                      # order sequence
            e[0], e[1] = e[1], e[0]                                          # swap
        
    positiveExamples = np.vstack({tuple(row) for row in positiveExamples})   # clear repetition 

    globalPositivePairs = []
    positivePairsWithLabel = []
    
    for e in positiveExamples:                                               # clear data 
        globalPositivePairs.append([e[0], e[1], 1])
        if (e[0] not in usersID) or (e[1] not in usersID) or (e[0] == e[1]):    
            continue
        positivePairsWithLabel.append([e[0], e[1], 1])
    
    np.savetxt("global_Positive_Examples", sorted(list(globalPositivePairs)), fmt="%s", delimiter="\t" )
    np.savetxt("positive_Examples", sorted(list(positivePairsWithLabel)), fmt="%s", delimiter="\t" )


if __name__ == '__main__': 
    getPositive()
