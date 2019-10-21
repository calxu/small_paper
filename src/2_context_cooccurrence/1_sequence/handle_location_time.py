#! /usr/bin/env python3

"""
Task: sort user id according by location, day
Author: Calvin,Xu
"""

import numpy as np
import sys


def read_file(filename):
    """ Read the Data. """
    dtype = [("User_ID", int), ("Date", int), ("Latitude", "S6"), ("Longitude", "S7")]                       # each column type
    vert1 = lambda x: int(x.decode()[:10].replace("-", "") + x.decode()[11:19].replace(":", ""))             # convert function
    vert2 = lambda x: x[:6]
    vert3 = lambda x: x[:7]
    data = np.genfromtxt(filename, dtype=dtype, delimiter="\t", converters={1: vert1, 2:vert2, 3:vert3}, usecols=(0, 1, 2, 3))

    return data                                                                                              # return the data


def cluster(data):
    """ Cluster data. """
    location = []                                           # the list of all location information
    data.sort( order=("Latitude", "Longitude", "Date") )    # sort according latitude and longitude
    document = []                                           # the list of document

    p = data[0]                                             # initialize the first element
    t = []                                                  # initialize the list
    t.append(p[0])                                          # add the first user id
    for e in data[1:]:                                      # traverse all data
        if p[2] == e[2] and p[3] == e[3]:                   # the same longitude and latitude
            t.append(e[0])                                  # add the user id
        else:
            document.append(t)                              # add the list t
            p = e                                           # set the prior value
            t = []                                          # clear the list t
            t.append(p[0])                                  # add the user id

    document.append(t)                                      # add the last one
    
    return document                                         # return the document
    

if __name__ == "__main__":
    data = read_file("../../1_imbalance_data/train_Checkins")                   # read the file
    document = cluster(data)                                # achieve the document
    for e1 in document:
        for e2 in e1:
            print(e2, end=" ")
        print()
