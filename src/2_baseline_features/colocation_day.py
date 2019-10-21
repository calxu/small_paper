#!/usr/bin/env python3
# encoding:utf8

"""
Task: Count
Author: Calvin,Xu
"""

import numpy as np
from math import log
import random
import time
import sys

def readCheckins():
    """ Read the checkins data. """
    filename = "../1_imbalance_data/train_Checkins"
    dtype = [("users_ID", int), ("time", "S10"), ("latitude", "S6"), ("longitude", "S7")]
    vert1 = lambda x: x[:10]
    vert2 = lambda x: x[:6]
    vert3 = lambda x: x[:7]
    checkins = np.genfromtxt(filename, dtype=dtype, delimiter="\t", converters={1: vert1, 2: vert2, 3: vert3}, usecols=(0, 1, 2, 3))

    return checkins


def usersRelationship(target):
    """ Read the relationship between two users. """
    filename = "../1_imbalance_data/" + target + "_Data"
    userPair = np.genfromtxt(filename, dtype=int, delimiter="\t")
    
    return userPair


def userCheckinsDict():
    """ Get user checkins dict. """
    userDict = dict()
    checkins = readCheckins()
    for e in checkins:
        if userDict.get(e[0]) == None:
            userDict[e[0]] = {(e[1],  e[2].decode() + "&" + e[3].decode())}
        else:
            userDict[e[0]].add((e[1], e[2].decode() + "&" + e[3].decode()))

    return userDict


def intersection(set01, set02):
    """ Get the intersection between two sets. """
    colocation = dict()
    for e1 in set01:
        for e2 in set02:
            if (e1[0] == e2[0]) and (e1[1] == e2[1]):
                if colocation.get(e1[1]) == None:
                    colocation[e1[1]] = 1
                else:
                    colocation[e1[1]] += 1

    return colocation


def usersCooccurrence(target):
    """ Get the cooccurrence information. """
    userDict = userCheckinsDict()
    userPair = usersRelationship(target)

    for e in userPair:
        timeLocation01 = userDict[e[0]]
        timeLocation02 = userDict[e[1]]
        colocation = intersection(timeLocation01, timeLocation02)
        
        allTimes = 0; diversity = 0
        if colocation == dict():
            diversity = 0
        else:
            for e1 in colocation:
                allTimes += colocation[e1]

            for e2 in colocation:
                z = colocation[e2]
                diversity += (-z/allTimes*log(z/allTimes,2))

        print(e[0], e[1], e[2], colocation, allTimes, diversity, sep="\t")


if __name__ == '__main__':
    usersCooccurrence(sys.argv[1])
