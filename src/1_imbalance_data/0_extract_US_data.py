#!/usr/bin/env python3
# encoding:utf8

"""
Task: Extract part US Checkin data.
Author: Calvin,Xu.
"""

import os
import numpy as np
import sys

def getCheckins():
    """ Get part US checkins data from total checkins. """
    filename = os.popen("ls ../ | grep 'totalCheckins.txt'").read().strip()
    totalCheckins = np.genfromtxt("../" + filename, dtype=str, delimiter='\t')
    
    USCheckins = []

    for e in totalCheckins:
        latitude = float(e[2])
        longitude = float(e[3])

        if (latitude >= 35) and (latitude <= 45) \
            and (longitude >= -90) and (longitude <= -74):
            USCheckins.append(e)

    np.savetxt("US_Checkins", USCheckins, fmt="%s", delimiter="\t")

    os.system("sort -nk 1 -k 2 US_Checkins > US_Checkins.bak")
    os.system("mv US_Checkins.bak US_Checkins")


if __name__ == "__main__":
    getCheckins()
