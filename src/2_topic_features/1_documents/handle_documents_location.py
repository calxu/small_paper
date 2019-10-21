#!/usr/bin/env python3
# encoding:utf8

"""
Task: Generate documents based on location.
Author: Calvin,Xu
"""

import numpy as np   

def readData():
    """ Read the checkins data. """
    dtype = [('userID', int), ("latitude", "S6"), ("longitude", "S7")]
    vert1 = lambda x: x[:6]; vert2 = lambda x: x[:7]
    data = np.genfromtxt('../../1_imbalance_data/train_Checkins', dtype=dtype, \
           converters={2:vert1, 3:vert2}, delimiter='\t', usecols=(0, 2, 3))
    return data


def cluster(data):
    """ Cluster the data according location. """
    location = [] 
    userID = set()
    for e in data:
        userID.add(int(e[0]))
        locationMark = e[1].decode() + " " + e[2].decode()
        location.append(locationMark)

    locationSet = set(location)        
    length = len(locationSet)                          # also mean the number of documents
    locationList = list(locationSet)      
    wordOfBag = [{} for i in range(length)]  

    noZeroNumber = 0
    for e in data:
        locationMark = e[1].decode() + " " + e[2].decode()
        i = locationList.index(locationMark) 
        if e[0] in wordOfBag[i].keys(): 
            wordOfBag[i][e[0]] += 1
        else:
            wordOfBag[i][e[0]] = 1
            noZeroNumber += 1

    # documents number; user number; the number of nozero element
    print(length, len(userID), noZeroNumber, sep="\t")

    i = 0
    for e in wordOfBag:
        # print(locationList[i], end="\t")             # print the location
        for m in e.keys():
            print(m, e[m], sep=":", end="\t" )         # key --- value
        i += 1 
        print()                                        # print line break


if __name__ == '__main__':
    data = readData()
    cluster(data)
