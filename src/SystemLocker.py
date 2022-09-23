#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#Author: Eric
#Date: 2019/05/10
# This is a locker in a system(OS).
#######################
#######################
import os
import time
import errno
import socket

class LockErr(Exception):
    pass

class FileLock(object):
    '''
    Use file of file.lock to judge if locked. Usage: with FileLock(filename): ...
    '''
    def __init__(self, file_name='FileLock', timeout=3, delay=0.1):
        self.is_locked = False
        self.lockfile = "%s.lock" % file_name
        self.timeout = timeout
        self.delay = delay

    def acquire(self):
        start_time = time.time()
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if (time.time() - start_time) >= self.timeout:
                    raise LockErr("File Lock Timeout occured.")
                time.sleep(self.delay)
        self.is_locked = True

    def release(self):
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False

    def __enter__(self):
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        if self.is_locked:
            self.release()

    def __del__(self):
        self.release()


def FileLocker(*args):
    Para = args
    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                with FileLock(*Para):
                    return func(*args, **kwargs)
            except LockErr as e:
                print (e)
            return
        return wrapper
    return deco 


class SocketLock(object):
    '''
    Use socket to judge if locked. Usage: with FileLock(filename): ...
    '''
    def __init__(self, socket_addr=('127.0.0.1', 8888), timeout=3, delay=0.1):
        self.is_locked = False
        self.socket_addr = socket_addr
        self.sk = None
        self.timeout = timeout
        self.delay = delay
    
    def acquire(self):
        self.sk = socket.socket()
        start_time = time.time()
        while True:
            try:
                self.sk.bind(self.socket_addr)
                break
            except OSError:
                if (time.time() - start_time) >= self.timeout:
                    raise LockErr("File Lock Timeout occured.")
                time.sleep(self.delay)
            return
        self.is_locked = True
    
    def release(self):
        if self.is_locked and self.sk:
            self.sk.close()
            self.is_locked = False
    
    def __enter__(self):
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self.release()

    def __del__(self):
        self.release()


def SocketLocker(*args):
    Para = args
    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                with SocketLock(*Para):
                    return func(*args, **kwargs)
            except LockErr as e:
                print (e)
        return wrapper
    return deco


def test1():
    import threading
    ##
    Locker = SocketLock
    #Locker = FileLock
    ##
    def test_test():
        print ("sub thread is running...")
        with Locker():
            print ("sub thread acquire")
            time.sleep(1)
        print ("sub thread released!")
    t = threading.Thread(target=test_test)
    t.daemon = True
    ##
    print ("This is a test.")
    print ('')
    print ("Main is running...")
    with Locker():
        t.start()
        print ("Main acquired")
        time.sleep(1)
    print ('Main released!')
    time.sleep(3)
    print ("All done!")

def test2():
    import threading
    ##
    Locker = SocketLocker
    #Locker = FileLocker
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
    test1()
    test2()
    
    
