#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#Author: Eric
#Date: 2019/05/10
# You will get string(like password) with show *(or something else) instead of character.
#######################
#######################
from abc import ABCMeta, abstractmethod
import platform
import sys
import os
#
from src.quickscan.quickscan.quickscan.devices import Devices
from src.pydiskinfo.pydiskinfo_system import System
from src.pydiskinfo.pydiskinfo_cmd import str_system,str_physical_disk,str_partition,str_logical_disk


class BaseDiskInfo(object):
    def __init__(self):
        pass

    @abstractmethod
    def print_as_text(self):
        ''' Erase a device. '''


class WinDiskInfo(BaseDiskInfo):
    def __init__(self):
        super(WinDiskInfo, self).__init__()
        self._context = System()

    def print_as_text(self):
        print(str_system(self._context))
        for each_physical_disk in self._context['Physical Disks']:
            print(f'  {str_physical_disk(each_physical_disk, "Pipts")}')
            for each_partition in each_physical_disk["Partitions"]:
                print(f'    {str_partition(each_partition, "LDdtse")}')
                for each_logical_disk in each_partition["Logical Disks"]:
                    print(f'      {str_logical_disk(each_logical_disk, "PpVtfF")}')


class LinDiskInfo(BaseDiskInfo):
    def __init__(self):
        super(LinDiskInfo, self).__init__()
        self._context = Devices(False)

    def print_as_text(self):
        print (self._context.report())


class AllDiskInfo(object):
    def __init__(self):
        self._os_type = platform.system()
        if self._os_type == "Windows":
            self.system = WinDiskInfo()
        elif self._os_type == "Linux":
            self.system = LinDiskInfo()
        else:
            raise RuntimeError("OS Not support!")

    def print_as_text(self):
        self.system.print_as_text()


