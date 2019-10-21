#!/usr/bin/env python3
# encoding:utf8

"""
Task: Generate negative examples.
Author: Calvin,Xu
"""

import numpy as np
import random    
import sys

sys.setrecursionlimit(1000000)

def DFS(Graph, user01):
    """ Depth traverse graph. """
    Graph['visited'][Graph['usersDict'][user01]] = True
    Graph['vertexSet'].add(user01)
    for user02 in Graph["usersID"]:
        if (Graph["graphDict"].get((user01, user02)) == 1) and \
           (Graph['visited'][Graph['usersDict'][user02]] == False):
            DFS(Graph, user02)


def getTotalNegatives():
    """ Get total negatives. """
    positiveExamples = np.genfromtxt("positive_Examples", dtype=int, delimiter='\t', usecols=(0, 1))
    positiveExamples = set([tuple(row) for row in positiveExamples])
    
    # users id map to index
    usersDict = dict()
    usersID = np.genfromtxt("users_ID", dtype=int)
    for index, user in enumerate(usersID, 0):
        usersDict[user] = index
    
    # graph representation
    graphDict = dict()
    for userPair in positiveExamples:
        graphDict[(userPair[0], userPair[1])] = 1
        graphDict[(userPair[1], userPair[0])] = 1

    visited = [False] * len(usersID)
    vertexesList = []

    # search connected subgraph
    for user in usersID:
        vertexSet = set()
        Graph = {"graphDict": graphDict, "usersID": usersID, "usersDict": usersDict, 
                 "visited": visited, 'vertexSet': vertexSet}
        
        if visited[usersDict[user]] == False:
            DFS(Graph, user)
            print(vertexSet)


if __name__ == '__main__':
    vertexesList = getTotalNegatives()       # The parameter is train or test
