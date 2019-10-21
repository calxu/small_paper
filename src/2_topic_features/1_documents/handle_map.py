#!/usr/bin/env python3

import sys
import numpy as np 


def read_user():
    """ Read user information. """
    Vocabulary = np.genfromtxt("Vocabulary", dtype=np.int, delimiter="\t")
    
    userDict = {}
    for index, userid in enumerate(Vocabulary):      # struct directory
        userDict[userid] = index                    # directory valuation

    return userDict                                 # return userDict


def structMatrix(filename, userMap):
    """ Read documentsMatrix value. """
    with open(filename, "r") as f:
        documentsMatrix = f.readlines()
    
    print(documentsMatrix[0], end="")
    for s in documentsMatrix[1:]:
        # print(s[:-2])
        userDict = eval("{"+s[:-2].replace("\t", ",")+"}")             # translate them into directory
        
        for e in userDict:
            print(userMap[e], userDict[e], sep=":", end="\t")
        
        print()


def main(argv):
    """ main function. """
    userDict = read_user()                          # user mapped to index     
    structMatrix(argv[1], userDict)                 # struct documents matrix


if __name__ == '__main__':
    main(sys.argv)                                   # main function
