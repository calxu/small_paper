#! /usr/bin/python3

"""
Task: sort user id according by day, location
Author: Calvin,Xu
"""

import numpy as np    
import math


def read_file(filename):
    """ Read the data. """
    dtype = [("User_ID", int), ("Date", int), ("Latitude", float), ("Longitude", float)]                     # each column type
    vert = lambda x: int(x.decode()[:10].replace("-", ""))                                                   # day convert function
    data = np.genfromtxt(filename, dtype=dtype, delimiter="\t", converters={1: vert}, usecols=(0, 1, 2, 3))  # read the data
    return data                                                                                              # return the data


def min_distance(q, article):
    """ Compute the distance between current point and previous points. """
    article.remove(q[-1])                                  # remove specific element from article
    p = (q[-1][1], q[-1][2])                               # the mean value of the already value
    min_value = 1000                                       # min_value user id and min value
    for e in article:                                      # traverse all word in article 
        distance = math.sqrt((p[0] - e[1]) ** 2 + (p[1] - e[2]) ** 2)       # the distance of two location
        if distance < min_value:                                            # the value smaller than min_value
            point = tuple(e)                                                # replace the point of min value
            min_value = distance                                            # replace the min value
    return point                                           # return the user id of min value (tuple type)
    

def cluster(data):
    """ Cluster data. """
    location = []                                          # the list of all location information
    data.sort( order=("Date", "Latitude", "Longitude") )   # sort according latitude and longitude

    document = []                                          # the list of document
    p = data[0]                                            # initialize the first element
    t = []                                                 # initialize the list
    t.append( (p[0], p[2], p[3]) )                         # add the first user id
    for e in data[1:]:                                     # traverse all data
        if p[1] == e[1]:                                   # the same longitude and latitude
            t.append( (e[0], e[2], e[3]) )                 # add the user id
        else:                                               
            document.append(t)                             # add the list t
            p = e                                          # set the prior value
            t = []                                         # clear the list t
            t.append( (p[0], p[2], p[3]) )                 # add the user id

    document.append(t)                                     # add the last one

    # rank the every document
    for article in document:                               # traverse all document
        q = []                                             # initialize the empty list q
        p = article[0]                                     # the first word of article
        q.append( p )                                      # add the first word of the article
        while len(article) != 1:                           # while article not equal 1
            m = min_distance(q, article)                   # compute the distance
            q.append( m )                                  # add the point m into the list q
    
        article[:] = q[:]                                  # copy the list q

    return document                                        # return the document


if __name__ == "__main__":
    data = read_file("../../1_imbalance_data/train_Checkins")        # read the file
    sequence = cluster(data)                                                              # achieve the document
    
    for e1 in sequence:                                        # use shell command to redirect
        for e2 in e1:
            print(e2[0], end=" ")
        print()
