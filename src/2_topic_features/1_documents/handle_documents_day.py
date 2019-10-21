#!/usr/bin/env python3
# encoding:utf8

"""
Task: Generate documents based on day.
Author: Calvin,Xu
"""

import numpy as np

def readData():
    """ Read the checkins data. """
    data = np.genfromtxt('../../1_imbalance_data/train_Checkins', dtype=str , delimiter='\t', usecols=(0, 1, 2, 3)) 
    return data


def cluster(data):
    """ Cluster the data according day period. """
    day = []
    userID = set()
    for e in data:
        userID.add(int(e[0]))
        day.append(e[1].split('T')[0]) 

    daySet = set(day)
    length = len(daySet)                              # also mean the number of documents
    dayList = list(daySet)
    wordOfBag = [{} for i in range(length)]       

    noZeroNumber = 0
    for e in data:
        time = e[1].split('T')[0]
        i = dayList.index(time)                       # achieve the index of documents
        if e[0] in wordOfBag[i].keys():               # the user in dictionary
            wordOfBag[i][e[0]] += 1 
        else:
            wordOfBag[i][e[0]] = 1
            noZeroNumber += 1
    
    # documents number; user number; the number of nozero element
    print(length, len(userID), noZeroNumber, sep="\t")
    
    i = 0
    for e in wordOfBag:
        # print(dayList[i], end="\t")                 # print the day
        for m in e.keys():
            print(m, e[m], sep=":", end="\t")         # key --- value
        i += 1 
        print()                                       # print line break


if __name__ == '__main__':
    data = readData()
    cluster(data)
