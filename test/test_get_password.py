#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append("..")
from src.GetPassword import getpass

def test():
    print ("This is a test.")
    passwd = getpass('Your password: ')
    print ("Password: %s" % passwd)


if __name__ == "__main__":
    test()
