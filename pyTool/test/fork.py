import os
import sys

pid = os.fork()

if pid == 0:
    print 'current process is child:',os.getpid(),'--parent process is:',os.getppid()
else:
    print 'current process is parent:', os.getpid(), '--child process is:', pid