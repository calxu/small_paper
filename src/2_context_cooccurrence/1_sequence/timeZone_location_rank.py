#!/usr/bin/python3
# encoding:utf8

"""
Task: Sort users id according time zone firstly. During the same time zone, sort 
      location zone according distance shortest principle.
Author: Calvin,Xu.
"""

import numpy as np    
import math
import time
import sys
from geopy.distance import great_circle

def readCheckins(filename):
    """ Read the checkins data. """
    dtype = [("users_ID", int), ("time", float), ("latitude", float), ("longitude", float)]                 # each column type
    vert = lambda x: time.mktime(time.strptime(x.decode(), '%Y-%m-%dT%H:%M:%SZ'))                           # convert to unix time
    data = np.genfromtxt(filename, dtype=dtype, delimiter="\t", converters={1: vert}, usecols=(0, 1, 2, 3)) # read the data
    return data 


def min_distance(q, article):
    """ Compute the distance between current point and previous points. """
    article.remove(q[-1])                                  # remove specific element from article
    q = np.array(q)                                        # translate into numpy type
    p = (q[:, 1].sum() / len(q) ,  q[:, 2].sum() / len(q)) # the mean value of the already value
    min_value = 9999999999                                 # min_value user id and min value
    for e in article:                                      # traverse all word in article 
        # distance = math.sqrt((p[0] - e[1]) ** 2 + (p[1] - e[2]) ** 2)       
        distance = great_circle((p[0], p[1]), (e[1], e[2])).meters              # the distance of two location
        if distance < min_value:                                            # the value smaller than min_value
            point = tuple(e)                                                # replace the point of min value
            min_value = distance                                            # replace the min value
    return point                                           # return the user id of min value (tuple type)
    

def clusterTimeZone(data, timeGranularity):
    """ Cluster time zone according checkins time. """
    location = []                               # the list of all location information
    data.sort(order=("time"))                   # sort according checkins time
    
    sequence = []                               # the list of sequence
    p = data[0]                                 # initialize the first element
    t = []                                      # initialize the list
    t.append( (p[0], p[2], p[3]) )              # add the first user id
    for e in data[1:]:
        if e[1] - p[1] <= timeGranularity:      # time zone smaller than timeGranularity
            t.append( (e[0], e[2], e[3]) )      # add the user id
        else:                                               
            sequence.append(t)
            p = e                               # set the prior value
            t = []                              # clear the list t
            t.append( (p[0], p[2], p[3]) )      # add the user id

    sequence.append(t)                          # add the last one
    
    # rank the every sequence
    for subset in sequence:
        q = []
        p = subset[0]                           # choose the first element of subset randomly
        q.append(p)
        while len(subset) != 1:                 # while subset not equal 1
            m = min_distance(q, subset)         # compute the distance
            q.append(m)                         # add the point m into the list q
    
        subset[:] = q[:]                        # copy the list q
    
    return sequence                             # return the sequence


if __name__ == "__main__":
    checkinsData = readCheckins("../train_Checkins")           # read the checkins data.
    timeGranularity = float(sys.argv[1])                       # parameter
    sequence = clusterTimeZone(checkinsData, timeGranularity)  # achieve the sequence.
    
    for e1 in sequence:                                        # use shell command to redirect
        for e2 in e1:
            print(e2[0], end=" ")
        print()
