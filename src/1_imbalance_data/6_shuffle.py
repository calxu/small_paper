#!/usr/bin/env python
# encoding:utf8

"""
Task: Merge positive and negative example.
Author: Calvin,Xu.
"""

import numpy as np
import sys
import os

def shuffle(target):
    """ Shuffle the sequence. """
    # if (target == "train"):
    #     os.system("awk 'BEGIN{srand()}{b[rand()NR]=$0}END{for(x in b)print b[x]}' train_Negatives \
    #                > train_Negatives.bak; rm train_Negatives; \
    #                head -n 8000000 train_Negatives.bak > train_Negatives")

    positive_example = np.genfromtxt(target + "_Positives", dtype=str, delimiter="\t")    # positive example data
    negative_example = np.genfromtxt(target + "_Negatives", dtype=str, delimiter="\t")    # negative example data

    data = np.vstack((positive_example, negative_example))           # all data
    
    np.random.shuffle(data)                                          # shuffle

    np.savetxt(target + "_Data", data, fmt="%s", delimiter="\t")     # save file


if __name__ == '__main__':
    shuffle(sys.argv[1])
