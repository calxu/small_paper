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
            vertexesList.append(vertexSet)

    return vertexesList


def getTrainTestNegatives(vertexesList):
    """ Get train and test negatives. """
    users_ID = np.genfromtxt("users_ID", dtype=int)
    usersSet = {row for row in users_ID}

    trainUsersID = np.genfromtxt("train_UsersID", dtype=int)
    trainUsersID = set(trainUsersID)

    testUsersID = np.genfromtxt("test_UsersID", dtype=int)
    testUsersID = set(testUsersID)

    trainNegativeExamples = set()
    testNegativeExamples = set()

    i = 0
    for userSet01 in vertexesList:
        print(userSet01)
        if len(userSet01) == 1:
            continue
        userSet01 = {list(userSet01)[random.randint(0, len(userSet01)-1)]}
        userSet01 = userSet01.intersection(usersSet)

        userList01 = list(userSet01)
        i += 1
        for userSet02 in vertexesList[i:]:
            if len(userSet02) == 1:
                continue
            userSet02 = {list(userSet02)[random.randint(0, len(userSet02)-1)]}
            userSet02 = userSet02.intersection(usersSet)
            if userSet01 == set() or userSet02 == set():
                continue

            userList02 = list(userSet02)
            for user01 in userList01:
                for user02 in userList02:
                    if (user01 in trainUsersID) and (user02 in trainUsersID):
                        trainNegativeExamples.add((user01, user02, 0))
                    elif (user01 in testUsersID) and (user02 in testUsersID):
                        testNegativeExamples.add((user01, user02, 0))

    np.savetxt("train_Negatives", np.array(list(trainNegativeExamples)), fmt="%s", delimiter='\t')
    np.savetxt("test_Negatives", np.array(list(testNegativeExamples)), fmt="%s", delimiter='\t')


if __name__ == '__main__':
    vertexesList = getTotalNegatives()       # The parameter is train or test
    # vertexesList = []
    # for line in sys.stdin:
    #     vertexesList.append(eval(line.strip()))
        
    getTrainTestNegatives(vertexesList)
