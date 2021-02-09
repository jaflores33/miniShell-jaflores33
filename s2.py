#! /usr/bin/env python3
import sys, os, re

def amper(args):
    print('ampersand\n')
    fd = os.fork()
    args.pop()

    if(fd==0):
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s"%(dir,args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
    else:
        return None

def defa(args):
    print('no ampersand\n')
    fd = os.fork()

    if(fd==0):
        p = True
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s"%(dir,args[0])
            try:
                os.execve(program, args, os.environ)
                p = True
            except FileNotFoundError:
                p = False
                pass
        if(p==False):
            print('Command not found\n')
    elif(fd<0):
        print('Something went wrong: ' + fd)
    else:
        os.wait()

def chDr(args):
    wd = os.getcwd()
    print('change the directory\n'+wd)
    nd = (wd + '/' + args[1])
    try:
        os.chdir(nd)
    except:
        print('No such directory')

def pipeFl(args):
    print('A pipe is being summoned\n')

    fd = os.fork()
    rd, wr = os.pipe()
    for f in (rd, wr):
        os.set_inheritable(f, True)
    
    if(fd==0):
        os.close(1)
        os.dup(wr)
        for fd in (rd,wr):
            os.close(fd)
        defa(args[0])
    elif(fd>0):
        os.close(0)
        os.dup(rd)
        for fd in (rd,wr):
            os.close(fd)
        defa(args[1])

def pipeFlag(args):
    print('pipe detected\n')
        
while(1):
    cmd = input('$$$$')
    if(cmd == 'exit'):
        exit()
    else:
        
        args = cmd.split()
        if(args[-1]=='&'):
            amper(args)
        elif('|' in cmd):
            ends = cmd.split('|')
            pipeFlag(ends)
        elif(args[0]=='cd'):
            chDr(args)
        else:
            defa(args)

exit()
