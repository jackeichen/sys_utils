#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#Author: Eric
#Date: 2019/05/10
# You will get string(like password) with show *(or something else) instead of character.
#######################
#######################
import sys,platform
os = platform.system()
pwd_input = None

##
class OSNotSupport(Exception):
    pass


# init windows
if os == 'Windows':
    import msvcrt
    def pwd_input(maskchar="*"):  
        chars = [] 
        while True:
            try:
                newChar = msvcrt.getch().decode(encoding="utf-8")
            except Exception as e:
                print (e)
                return input("you will get plain text while typing: ")
            if newChar in '\r\n':
                print ('')
                break 
            elif newChar == '\b':
                if chars:
                    del chars[-1] 
                    msvcrt.putch('\b'.encode(encoding='utf-8'))
                    msvcrt.putch( ' '.encode(encoding='utf-8'))
                    msvcrt.putch('\b'.encode(encoding='utf-8'))                
            else:
                chars.append(newChar)
                msvcrt.putch(maskchar.encode(encoding='utf-8'))
        return (''.join(chars) )

# init linux
if os == 'Linux':
    import tty,termios
    def getch():  
        fd = sys.stdin.fileno() 
        old_settings = termios.tcgetattr(fd) 
        try: 
            tty.setraw(sys.stdin.fileno()) 
            ch = sys.stdin.read(1) 
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
        return ch

    def pwd_input(maskchar="*"): 
        password = "" 
        while True: 
            ch = getch() 
            if ch == "\r" or ch == "\n": 
                print ('')
                return password 
            elif ch == "\b" or ord(ch) == 127: 
                if len(password) > 0: 
                    sys.stdout.write("\b \b") 
                    sys.stdout.flush()
                    password = password[:-1] 
            else: 
                if maskchar != None: 
                    sys.stdout.write(maskchar)
                    sys.stdout.flush()
                password += ch
        return password
#######################
def getpass(prompt='', maskchar="*"):
    '''
    Input:
        var                    description
        prompt                 You can give a prompt
        maskchar               Character that show instead of the real one
    Return:
        the real password.(string type)
    '''
    if not pwd_input:
        raise OSNotSupport("OS not support: %s" % os)
    sys.stdout.write(str(prompt))
    sys.stdout.flush()
    return pwd_input(maskchar)
