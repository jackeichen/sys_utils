#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append("..")
from src.DiskScan import AllDiskInfo

def test():
    test = AllDiskInfo()
    test.print_as_text()


if __name__ == "__main__":
    test()
