#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append("..")
import threading
import time

from src.SystemLocker import SocketLock,FileLock,SocketLocker,FileLocker


def test1(Lock):
    ##
    # Locker = SocketLock
    #Locker = FileLock
    ##
    def test_test():
        print ("sub thread is running...")
        with Lock():
            print ("sub thread acquire")
            time.sleep(1)
        print ("sub thread released!")
    t = threading.Thread(target=test_test)
    t.daemon = True
    ##
    print ("This is a test.")
    print ('')
    print ("Main is running...")
    with Lock():
        t.start()
        print ("Main acquired")
        time.sleep(1)
    print ('Main released!')
    time.sleep(3)
    print ("All done!")

def test2(Locker):
    ##
    # Locker = SocketLocker
    # Locker = FileLocker
    ##
    @Locker()
    def test_sub():
        print ("sub thread is running...")
        time.sleep(1)
        return 0
    t = threading.Thread(target=test_sub)
    t.daemon = True
    @Locker()
    def test_main():
        print ("Main is running...")
        t.start()
        time.sleep(4)
    ##
    print ("This is a test.")
    print ('')
    test_main()
    time.sleep(3)
    print ("All done!")


if __name__ == "__main__":
    test1(SocketLock)
    test1(FileLock)
    test2(SocketLocker)
    test2(FileLocker)
