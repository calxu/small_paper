#!/usr/bin/env python3
# encoding:utf8

"""
Task: Get users id and train checkins.
Author: Calvin,Xu.
"""

import os
import numpy as np
import sys

def getUsers(leastCheckins):
    """ get usersID according users checkins >= leastCheckins. """
    os.system("cut -d'	' -f1 US_Checkins | sort -n > US_IDs")
    with open("./US_IDs", "r") as f:
        usersCheckins = f.readlines()

    # the number of checkins should be larger than 5
    usersCheckinsDict = dict()
    usersCheckinsSet = set()
    for e in usersCheckins:
        if usersCheckinsDict.get(e) == None:
            usersCheckinsDict[e] = 1
        else:
            usersCheckinsDict[e] += 1

    for e in usersCheckinsDict:
        if usersCheckinsDict[e] >= leastCheckins:
            usersCheckinsSet.add(e)

    # save data
    with open("./users_ID", "w") as f:
        f.writelines(usersCheckinsSet)

    os.system("rm US_IDs")
    os.system("sort -n users_ID | uniq > users_ID.bak")
    os.system("rm users_ID; mv users_ID.bak users_ID")

    # global user id
    filename = os.popen("ls ../ | grep 'edges.txt'").read().strip()
    os.system("cut -d'	' -f1 ../" + filename + " | sort -n | uniq > global_users_ID")
    os.system("cut -d'	' -f2 ../" + filename + " | sort -n | uniq >> global_users_ID")
    os.system("sort -n global_users_ID | uniq > global_users_ID.bak")
    os.system("mv global_users_ID.bak global_users_ID")


def getCheckins():
    """ Get train checkins. """
    filename = os.popen("ls | grep 'US_Checkins'").read().strip()
    totalCheckins = np.genfromtxt(filename, dtype=str, delimiter='\t')
    usersID = np.genfromtxt("users_ID", dtype=str)

    usersID = set(usersID)
    trainCheckins = []
    for e in totalCheckins:
        if e[0] in usersID:
            trainCheckins.append(e)

    np.savetxt("train_Checkins", trainCheckins, fmt="%s", delimiter="\t")

    os.system("rm US_Checkins")


if __name__ == "__main__":
    getUsers(int(sys.argv[1]))
    getCheckins()
